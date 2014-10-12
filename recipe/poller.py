#!/usr/bin/env python

"""
The script that runs every X minutes and checks if new events are raised and
corresponding actions have to be triggered.

Script is intentionally django-agnostic and relies on raw SQL.
"""

import json
import psycopg2
import psycopg2.extras
import importlib
import datetime

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    trigger_module = importlib.import_module("trigger.triggers")
    action_module = importlib.import_module("action.actions")

    conn = psycopg2.connect("dbname=ifttt user=theju")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM channel_channel")
    channels = cursor.fetchall()

    cursor.execute("SELECT * FROM trigger_trigger")
    triggers = cursor.fetchall()

    cursor.execute("SELECT * FROM action_action")
    actions = cursor.fetchall()

    triggers_by_id = {}
    for trigger_row in triggers:
        trigger = {"obj": getattr(trigger_module, trigger_row["klass"])()}
        trigger.update(trigger_row)
        triggers_by_id[trigger["id"]] = trigger

    actions_by_id = {}
    for action_row in actions:
        action = {"obj": getattr(action_module, action_row["klass"])()}
        action.update(action_row)
        actions_by_id[action["id"]] = action

    cursor.execute("SELECT * FROM recipe_recipe")
    recipes = cursor.fetchall()
    recipe_update = []
    # TODO: Move to gevent to prevent blocking on IO
    for recipe in recipes:
        trigger_id = recipe["trigger_id"]
        action_id  = recipe["action_id"]
        trigger = triggers_by_id[trigger_id]
        action = actions_by_id[action_id]
        trigger_fn = trigger["obj"].trigger
        params = {"trigger": json.loads(recipe["trigger_params"])}
        event_triggered = trigger_fn(recipe, **params)
        if event_triggered:
            action_fn  = action["obj"].action
            params.update({"action": json.loads(recipe["action_params"])})
            success = action_fn(recipe, **params)
            if success:
                recipe_update.append((datetime.datetime.now(), recipe["id"]))
    if recipe_update:
        cursor.executemany("UPDATE recipe_recipe SET last_checked=%s "
                           "WHERE id=%s", recipe_update)
        conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
