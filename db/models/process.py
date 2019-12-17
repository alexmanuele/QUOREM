from collections import defaultdict

from django.db import models
from django.apps import apps

#for searching
from django.contrib.postgres.search import SearchVector
from django.contrib.contenttypes.models import ContentType
from db.models.object import Object

from combomethod import combomethod

class Process(Object):
    base_name = "process"
    plural_name = "processes"

    gv_node_style = {'style': 'rounded,filled', 'shape': 'box', 'fillcolor': '#ffd4d4'}

    description = "A set of Steps run with a typical series of Parameters"

    has_upstream = True

    name = models.CharField(max_length=255, unique=True)

    upstream = models.ManyToManyField('self', symmetrical=False, related_name="downstream", blank=True)
    all_upstream = models.ManyToManyField('self', symmetrical=False, related_name='all_downstream', blank=True)

    values = models.ManyToManyField('Value', related_name="processes", blank=True)

    def get_parameters(self, steps=None, step_field="pk"):
        Parameter = apps.get_model("db.Parameter")
        if steps is None:
            steps = self.steps.all()
#        else:
#            steps = self.steps.filter(pk__in=steps)
        params = {}
        for step in steps:
            proc_params = dict([(x.signature.get().name,
                                (x, 'process'))
                                for x in self.values.instance_of(Parameter).filter(steps=step, results__isnull=True, analyses__isnull=True)])
            step_params = step.get_parameters()[step.pk]
            proc_params.update(step_params)
            if not proc_params:
                proc_params = {}
            params[getattr(step, step_field)] = proc_params
        return params

    def auto_add_steps(self):
        source_steps = apps.get_model("db.Step").objects.filter(pk__in=self.analyses.values("results__source_step__pk"))
        self.steps.add(*source_steps)

    def add_steps(self, steps):
        self.steps.add(*apps.get_model("db.Step").objects.filter(pk__in=steps))

    @classmethod
    def update_search_vector(cls):
        cls.objects.update(
            search_vector = (SearchVector('name', weight='A')
        ))

    def related_steps(self, upstream=False):
        steps = self.steps.all()
        if upstream:
            steps = steps | apps.get_model("db", "Step").objects.filter(pk__in=steps.values("all_upstream").distinct())
        return steps

    def related_analyses(self):
        return self.analyses.all()
