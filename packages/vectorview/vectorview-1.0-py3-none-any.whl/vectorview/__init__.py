from typing import Any, Optional, Dict
import requests
import inspect

def output_is_dict(output):
    if isinstance(output, dict): 
        if all(isinstance(key, str) for key in output):
            return True
        return False
    return False

class Vectorview:
    def __init__(self, pipeline_id: str, version_name: str = None) -> None:
        self.pipeline_id = pipeline_id
        self.version_name = version_name
        self.evaluators = []
        self.trace_id = None
        self.test_run_id = None

        payload = {
            "pipeline_id": pipeline_id,
        }
        response = requests.post('http://app.vectorview.ai/api/get_evaluators', json=payload)
        if response.status_code == 200:
            self.evaluators = response.json()
        else:
            print("Get evaluators Error:", response.text)

    def _add_code(self, pipeline_code):
        payload = {
            "pipeline_id": self.pipeline_id,
            "code": pipeline_code,
        }
        response = requests.post('http://app.vectorview.ai/api/add_code', json=payload)
        if response.status_code == 200:
            return response.json()["code_id"] 
        else:
            print("Add trace Error:", response.text)

    def _start_trace(self, pipeline_code):
        code_id = self._add_code(pipeline_code)
        payload = {
            "pipeline_id": self.pipeline_id,
            "version_name": self.version_name,
            "test_run_id": self.test_run_id,
            "code_id": code_id,
        }
        response = requests.post('http://app.vectorview.ai/api/add_trace', json=payload)
        if response.status_code == 200:
            self.trace_id = response.json()["trace_id"] 
        else:
            print("Add trace Error:", response.text)

    def _add_span(self, name: str, value: Optional[Any] = None, span_type: Optional[str] = "event") -> None:
        payload = {
            "trace_id": self.trace_id,
            "name": name,
            "value": value,
            "span_type": span_type
        }
        response = requests.post('http://app.vectorview.ai/api/add_span', json=payload)
        if response.status_code != 200:
            print("Add span Error:", response.text)

    def track(self, name: str, value: Optional[Any] = None) -> None:
        self._add_span(name, value)

    def add_target(self, target) -> None:
        if output_is_dict(target):
            for name, value in target.items():
                self._add_span(name, value, "target")
        else:
            self._add_span("target", output, "target")

    def set_metadata(self, metadata):
        payload = {
            "trace_id": self.trace_id,
            "key": "metadata",
            "value": metadata,
        }
        response = requests.post('http://app.vectorview.ai/api/update_trace', json=payload)
        if response.status_code != 200:
            print("Set metadata Error:", response.text)

    def set_session(self, session_id):
        payload = {
            "trace_id": self.trace_id,
            "key": "session_id",
            "value": session_id,
        }
        response = requests.post('http://app.vectorview.ai/api/update_trace', json=payload)
        if response.status_code != 200:
            print("Set session Error:", response.text)

    def set_user(self, end_user_id):
        payload = {
            "trace_id": self.trace_id,
            "key": "end_user",
            "value": end_user_id,
        }
        response = requests.post('http://app.vectorview.ai/api/update_trace', json=payload)
        if response.status_code != 200:
            print("Set user Error:", response.text)

    def mark_test(self, dataset_id, name=None):
        payload = {
            "dataset_id": dataset_id,
            "name": name,
        }
        response = requests.post('http://app.vectorview.ai/api/add_test_run', json=payload)
        if response.status_code == 200:
            self.test_run_id = response.json()["test_run_id"] 
        else:
            print("Add test run Error:", response.text)

    def _close_trace(self):
        if len(self.evaluators) == 0:
            print("Warning, no evaluators")
        else:
            for evaluator in self.evaluators:
                payload = {
                    "trace_id": self.trace_id,
                    "evaluator_id": evaluator
                }
                response = requests.post('http://app.vectorview.ai/api/add_job', json=payload)
                if response.status_code != 200:
                    print("Add job Error:", response.text)


def pipeline_decorator(vv):
    def decorator(func):
        def wrapper(*args, **kwargs):
            pipeline_code = inspect.getsource(func)
            vv._start_trace(pipeline_code)

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            for name, value in bound_args.arguments.items():
                vv._add_span(name, value, "input")

            output = func(*args, **kwargs)

            if output_is_dict(output):
                for name, value in output.items():
                    vv._add_span(name, value, "output")
            else:
                vv._add_span("output", output, "output")

            vv._close_trace()

            return output
        return wrapper
    return decorator

#TODO: make part of VV class
def get_dataset(name, pipeline_id):
    payload = {
        "pipeline_id": pipeline_id,
        "name": name,
    }
    response = requests.post('http://app.vectorview.ai/api/get_dataset', json=payload)
    if response.status_code == 200:
        dataset = response.json()["dataset"]
        dataset_id = response.json()["dataset_id"]
        return dataset, dataset_id
    else:
        print("Get dataset Error:", response.text)
