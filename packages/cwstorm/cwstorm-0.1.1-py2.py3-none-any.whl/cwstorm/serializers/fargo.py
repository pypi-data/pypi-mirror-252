def serialize(node):
    node_type = node.__class__.__name__.lower()
    elements = []
    element = {}
    element["name"] = node.name()
    element["label"] = node.name()
    element["type"] = node_type
    if node_type == "job":
        element.update(get_job_attrs(node))
    else:
        element.update(get_task_attrs(node))

    element["dependencies"] = [c.name() for c in node.children]
    elements.append(element)

    for c in node.children:
        elements.extend(serialize(c))

    return elements


def get_job_attrs(job):
    attrs = {}
    attrs["comment"] = job.comment()
    attrs["author"] = job.author()
    attrs["created_at"] = job.created_at()
    attrs["schema_version"] = job.schema_version()
    attrs["metadata"] = job.metadata()
    attrs["project"] = job.project()
    return attrs


def get_task_attrs(task):
    attrs = {}
    attrs["commands"] = [dict(c) for c in task.commands()]
    attrs["hardware"] = task.hardware()
    attrs["lifecycle"] = task.lifecycle()
    attrs["attempts"] = task.attempts()
    attrs["env"] = task.env()
    attrs["initial_state"] = task.initial_state() or "START"
    return attrs
