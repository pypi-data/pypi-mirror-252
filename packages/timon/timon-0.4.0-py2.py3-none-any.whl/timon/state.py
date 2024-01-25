#!/usr/bin/env python
"""
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         timon.state
#
# Description:  state object for timon
#
# #############################################################################
"""

import json
import logging
import os
import pickle
import time
from heapq import heapify
from heapq import heappop
from heapq import heappush
from heapq import heapreplace

from timon.probes.probe_if import mk_probe
from timon.probes.probes import resources

logger = logging.getLogger(__name__)
localopen = open  # for testing / mocking


class TMonQueue(object):
    def __init__(self, state):
        self.heap = []
        self.state = state  # just in case
        self.probes = state.probes
        self.sched_dict = {}
        cfg = self.state.state['task_queue']
        self.probes = self.state.probes  # TODO: really a copy here?
        self.sched_dict = cfg['sched_dict']
        self.heap[:] = cfg['heap']

    def add(self, sched_entry):
        """ adds an entry to the scheduler """
        name = sched_entry['name']
        logger.debug("Add Entry[%s] = %s", name, sched_entry)
        self.sched_dict[name] = sched_entry
        heappush(self.heap, [sched_entry['t_next'], name])

    def pop(self):
        """ gets/and removes an entry from the scheduler """
        t, sched_entry = heappop(self.heap)
        sched = self.sched_dict.pop(sched_entry)
        return t, sched

    def add_get(self, push_entry):
        """ adds entry to scheduler and gets one """
        t, sched_entry = heappop(self.heap)
        self.sched_dict.pop(sched_entry)
        t, sched_entry = push_entry
        t, sched_entry = heapreplace(self.heap, push_entry)
        self.sched_dict[sched_entry] = sched_entry

    def get_expired(self, t_exp, do_pop=True):
        if do_pop:  # caller just as to push new values
            while True:
                t, probe_id = self.heap[0]
                if t > t_exp:
                    return
                yield self.pop()
        else:  # yield. caller must pop/push
            while True:
                t, probe_id = self.heap[0]
                if t > t_exp:
                    return
                yield t, probe_id  # to_push

    def get_probes(self, now=None, force=False):
        now = now if now else time.time()
        heap = self.heap
        pop = self.pop
        all_probes = self.probes
        logger.debug("get_probes (%d to examine)", len(heap))
        while True:
            if not heap or ((heap[0][0] > now) and not force):
                if heap:
                    logger.debug(
                        "H0 %s > %s (delta: %.1f). aborting",
                        str(heap[0]), now, heap[0][0] - now)
                break
            _t, entry = pop()
            entry = dict(entry)
            entry_name = entry["name"]
            probe_args = all_probes.get(entry_name)
            if probe_args is None:
                msg = "Probe %r not found. It might be obsolete" % entry_name
                logger.warning("%s", msg)
                continue
            entry.update(probe_args)
            cls_name = probe_args['cls']
            probe = mk_probe(cls_name, **entry)
            logger.debug("will yield %s", str(probe))
            yield probe

    def reschedule_probes(self, probenames, new_t_next):
        """
        Reschedule multiple probes to a new timestamp

        Args:
            probenames (list of str): list of probenames to reschedule
            new_t_next (float): the new timestamp
        """
        for item in self.heap:
            if item[1] in probenames:
                item[0] = new_t_next
                self.sched_dict[item[1]]["t_next"] = new_t_next
        heapify(self.heap)

    def __repr__(self):
        return "TMonQ<%d probes / %d entries/ %d in heap>" % (
            len(self.probes), len(self.sched_dict), len(self.heap))

    def __contains__(self, item):
        return item in self.sched_dict

    def is_empty(self):
        return not self.heap

    def items(self):
        for value in self.sched_dict.items():
            yield value

    def as_dict(self):
        """
        returns queue as a jsonable dict.
        Makes copy of heap and sched dict (caution: actually, no need of a deep
        copy so a simple copy is made)
        """
        copied_heap = self.heap.copy()
        copied_heap.sort()
        rslt = dict(heap=copied_heap, sched_dict=self.sched_dict.copy())
        return rslt

    def get_probe_n_schedule(self, probename):
        """
        Search probename in heap and returns info found in heap and sched_dict

        Args:
            probename (str): name of the probe to search
        """
        for item in self.heap:
            if item[1] == probename:
                return {"heap": item, "sched": self.sched_dict.get(probename)}
        return None

    def t_next(self):
        if self.heap:
            return self.heap[0][0]
        else:
            return 0

    def get_resources(self):
        return resources.get_all_resources()

    def __len__(self):
        return len(self.heap)


class TMonState(object):
    """ keeps track of timon's state
        like schedulers / etc
    """
    def __init__(self, state_file=None, config=None):
        self.fname = fname = state_file
        pfx, ext = os.path.splitext(fname)
        self.probest_fname = pfx + "_prb" + ext
        self.config = config
        self.probes = config.probes
        self.queue = None
        self.state = {}
        try:
            with localopen(fname) as fin:
                self.state = json.load(fin)
            self.merge_tmp_probe_state()
        except FileNotFoundError:
            self.reset_state()
            self.save()
            if os.path.exists(self.probest_fname):
                os.unlink(self.probest_fname)

    def merge_tmp_probe_state(self, clear_after_read=False):
        """ merges in probe intermediate probe state file
            the intermediate probe state file is a file, that is written during
            probe runs to have persistent state info.

            It's contents can be synchronized into the state file at given
            points in time.
        """
        entries = []
        try:
            with localopen(self.probest_fname, "rb") as fin:
                load = pickle.load
                while True:
                    entries.append(load(fin))
        except EOFError:
            if clear_after_read:
                os.unlink(self.probest_fname)
        except FileNotFoundError:
            pass
        for entry in entries:
            logger.debug(entry)
        if entries:
            1/0

    def get_queue(self):
        """ gets queue or update from state """
        if self.queue is not None:
            return self.queue
        self.queue = TMonQueue(self)
        return self.queue

    def save(self, safe=True):
        """ saves state to file
            :param safe: bool. If true file will be safely written.
                            This means: written to a temp file, being closed
                            and renamed. Thus another process reading will
                            never see a partial file
        """
        fname = self.fname
        logger.debug("Shall save state to %s", fname)
        if self.queue is not None:
            self.state['task_queue'] = self.queue.as_dict()
        else:
            self.state['task_queue'] = dict(heap=[], sched_dict={})

        logger.debug("len(task_queue[heap]) = %d", len(
            self.state["task_queue"]["heap"]))
        if self.state["task_queue"]["heap"]:
            logger.debug("last heap = %r", self.state["task_queue"]["heap"][0])
        if safe:
            partial_fname = fname + ".partial"
        else:
            partial_fname = fname
            fname = None
        now = time.time()
        with localopen(partial_fname, "w") as fout:
            self.state['mtime'] = now
            json.dump(self.state, fout, indent=1)
        if fname:
            os.rename(partial_fname, fname)

    def has_state_changed(self, probe, status, flap_detection=True,
                          flap_cnt=2):
        """
        Check if the probe state has changed between the current and the
        previous run.
        If flap detection is enabled, ensure there's <flap_cnt> successive
        similar results before considering the state has changed.

        Args:
            probe (Probe object): Probe to check
            status (str): state of the current run
            flap_detection (bool, optional): activate/deactivate flap
                detection. Defaults to True.
            flap_cnt (int, optional): Minimum successive similar results
                before considering state has changed (current state is
                counted in). Defaults to 2.

        Returns:
            bool: returns True if state has changed, False otherwise
        """
        probe_name = probe.name
        prb_states = self.state['probe_state']
        if probe_name not in prb_states:
            prb_states[probe_name] = []
        pst = prb_states[probe_name]
        if not pst:
            return True
        if not flap_detection:
            # Compare only with the previous status
            prev_status = pst[-1][1]
            return status != prev_status
        else:
            # FLAP DETECTION
            if len(pst) < flap_cnt:
                logger.info(
                    "Cannot flap detect the status changing of the probe %s,"
                    " results length (%d) is < at flappy_cnt (%d)",
                    probe_name, len(pst), flap_cnt
                )
                return False
            flap_window = pst[-flap_cnt+1:]
            for rslt in flap_window:
                if rslt[1] != status:
                    # Status has changed too quickly: Flappy
                    return False
            previous_rslt_to_compare = pst[-flap_cnt]
            return previous_rslt_to_compare[1] != status

    async def update_probe_state(
            self, probe,
            status, msg=None, t=None, save=False):
        """ updates a probe state
            :param save: will also be saved to disk for potential
                    web status / notifiers / etc.

            :returns True if state changed
        """
        t = t or time.time()
        probe_name = probe.name
        if save:
            raise NotImplementedError("save option is still not implemented")
        has_state_changed = self.has_state_changed(probe=probe, status=status)
        prb_states = self.state['probe_state']
        if probe_name not in prb_states:
            prb_states[probe_name] = []
        pst = prb_states[probe_name]
        prev_status = pst[-1][1] if pst else "UNKNOWN"
        pst.append((t, status, msg))
        pst[:] = pst[-10:]
        if self.config.dbstore:
            await self.config.dbstore.store_probe_result(
                probename=probe_name, timestamp=t, msg=msg, status=status
            )
            if has_state_changed:
                await self.config.dbstore.store_hist_probe_result(
                    probename=probe_name, timestamp=t, msg=msg, status=status
                )
        return status != prev_status

    def get_probe_state(self, probe):
        return self.state['probe_state'][probe.name]

    @staticmethod
    def mk_sched_entry(
            name, t_next=None, interval=None,
            failinterval=None, schedule=None):
        """ helper to create a new schedule entry """
        # TODO: some error must be here
        schedule = schedule or {}
        t_next = t_next or time.time()
        interval = interval or schedule.get('interval', 901)
        failinterval = failinterval or schedule.get('failinterval', 901)
        return dict(
            name=name,
            t_next=t_next,
            interval=interval,
            failinterval=failinterval,
            )

    def refresh_queue(self):
        """
        refreshes the queue.
        This has to be called under following conditions:
        - when a new config was loaded and new probes were added
        """
        logger.info("refresh queue")
        now_s = time.time()
        config = self.config
        queue = self.queue = self.get_queue()
        for probe in self.probes.values():
            probe_name = probe['name']
            if probe_name not in queue:
                logger.debug("Adding entry for %s", probe_name)
                sched = config.cfg['schedules'][probe['schedule']]
                sched_st = self.mk_sched_entry(
                    probe['name'],
                    t_next=now_s,
                    schedule=sched,
                    )
                queue.add(sched_st)

    def reset_state(self, now=None):
        """ create a completely new fresh state
            :param now: just for testing
        """
        now = now if now else time.time()
        self.state = dict(
            type="timon_state",
            version="0.0.1",
            ctime=now,
            mtime=now,
            task_queue=[],
            probe_state={},
        )
