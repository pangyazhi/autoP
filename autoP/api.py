from datetime import datetime

import Singleton as Singleton
from flask import render_template, redirect, url_for, flash, abort, request, jsonify
from flask_login import logout_user, login_required, login_user

from autoP.models import User, load_user, query_results
from forms import LoginForm, RegistrationForm, SearchForm
from . import app


@app.route('/get_task/<instance_id>', methods=['GET'])
def get_task(instance_id):
    step = InstanceManager.get_step(instance_id)
    if step is not None:
        return jsonify(step)
    return jsonify({'step': {'action': 'wait', 'data': '10'}})


@app.route('/set_result/<instance_id>', methods=['PUT'])
def set_result(instance_id):
    if not request.json:
        abort(400)
    instance_id = request.json['instance_id']
    result = {
        'id': request.json['id'],
        'result': request.json['result']
    }
    InstanceManager.add_result(instance_id, result)


class InstanceManager(metaclass=Singleton):
    def __init__(self):
        self.data = {}

    def add_instance(self, instance):
        """

        :type instance: Instance
        """
        id = str(instance._data['id'])
        if not self.data.has_key(id):
            self.data[id] = instance

    def add_step(self, instance_id, step):
        if not self.data.has_key(instance_id):
            raise OverflowError('Instance ' + instance_id + ' is not in the Instance Manager yet.')
        self.data[instance_id].add_step(step)

    def get_step(self, instance_id):
        if not self.data.has_key(instance_id):
            raise OverflowError('Instance ' + instance_id + ' is not in the Instance Manager yet.')
        self.data[instance_id].get_step()

    def add_result(self, instance_id, result):
        if not self.data.has_key(instance_id):
            raise OverflowError('Instance ' + instance_id + ' is not in the Instance Manager yet.')
        self.data[instance_id].add_result(result)
