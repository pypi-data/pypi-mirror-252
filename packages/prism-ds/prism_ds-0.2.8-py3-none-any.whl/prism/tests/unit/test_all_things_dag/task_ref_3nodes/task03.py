import prism.task


class Task03(prism.task.PrismTask):

    def run(self, tasks, hooks):
        return tasks.ref('task02') + "This is task 3."
