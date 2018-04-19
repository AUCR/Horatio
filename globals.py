# coding=utf-8
from app.plugins.tasks.models import TaskCategory
from yaml_info.yamlinfo import YamlInfo


def get_choices():
    available_choices = TaskCategory.query.all()
    return available_choices


run = YamlInfo("app/plugins/Horatio/detection_methods.yml", "none", "none")
detection_data = run.get()
count = 0
items_available_choices_list = []
for items in detection_data:
    count += 1
    new_list = (str(count), items)
    items_available_choices_list.append(new_list)
AVAILABLE_CHOICES = items_available_choices_list
