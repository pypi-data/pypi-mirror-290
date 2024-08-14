import traceback
from twisted.python import log
from copy import copy

from scrapyd.utils import JsonResource
from scrapyd.utils import native_stringify_dict



class WsResource(JsonResource):

    def __init__(self, root):
        JsonResource.__init__(self)
        self.root = root

    def render(self, txrequest):
        try:
            return JsonResource.render(self, txrequest).encode('utf-8')
        except Exception as e:
            if self.root.debug:
                return traceback.format_exc().encode('utf-8')
            log.err()
            r = {"node_name": self.root.nodename, "status": "error", "message": str(e)}
            return self.render_object(r, txrequest).encode('utf-8')


class JhCancel(WsResource):
    def render_POST(self, txrequest):
        args = {k: v[0] for k, v in native_stringify_dict(copy(txrequest.args), keys_only=False).items()}
        project = args['project']
        jobid = args['job']
        signal = args.get('signal', 'TERM')

        # 删除running
        _is_ok = self._rm_by_running(project, jobid, signal)

        prevstate = None
        if _is_ok:
            prevstate = 'running'
        else:
            _is_ok = self._rm_by_pending(project, jobid)
            if _is_ok:
                prevstate = 'pending'

        return {"node_name": self.root.nodename, "status": "ok" if _is_ok else "error", "prevstate": prevstate}

    def _rm_by_running(self, project, jobid, signal) -> bool:
        _is = False
        spiders = self.root.launcher.processes.values()
        for s in spiders:
            if s.project == project and s.job == jobid:
                s.transport.signalProcess(signal)
                _is = True
        return _is

    def _rm_by_pending(self, project, jobid) -> bool:
        # 创建调度对象
        queue = self.root.poller.queues[project]
        return queue.cancel(jobid)
