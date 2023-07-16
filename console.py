#!/usr/bin/python3
"""
This module defines the command interpreter.
"""

import cmd
import shlex
from datetime import datetime
import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """
    The command interpreter class for managing AirBnB objects.
    """
    prompt = '(hbnb) '

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Amenity": Amenity,
        "City": City,
        "State": State,
        "Review": Review,
        "Place": Place,
    }

    def do_quit(self, line):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """
        Handles the EOF signal to exit the program.
        """
        return True

    def emptyline(self):
        """
        Ignores empty lines.
        """
        pass

    def do_create(self, line):
        """
        Creates a new instance of a class.
        Usage: create <class name>
        """
        if not line:
            print("** class name missing **")
            return

        try:
            class_name = line.split()[0]
            obj = self.classes[class_name]()
            obj.save()
            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        Displays the string representation of an instance.
        Usage: show <class name> <id>
        """
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        storage = models.storage
        objects = storage.all()

        key = class_name + '.' + obj_id
        if key in objects:
            obj = objects[key]
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id>
        """
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        storage = models.storage
        objects = storage.all()

        key = class_name + '.' + obj_id
        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """
        Displays all instances of a class or all instances.
        Usage: all or all <class name>
        """
        args = shlex.split(line)
        objects = models.storage.all()

        if not args:
            print([str(obj) for obj in objects.values()])
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        print([
            str(obj) for obj in objects.values()
            if obj.__class__.__name__ == class_name
            ])

    def do_update(self, line):
        """
        Updates an instance based on the class name and id.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return

        obj_id = args[1]
        attr_name = args[2]
        attr_value = args[3].strip('"')

        storage = models.storage
        objects = storage.all()

        key = class_name + '.' + obj_id
        if key in objects:
            obj = objects[key]
            setattr(obj, attr_name, attr_value)
            obj.updated_at = datetime.now()
            storage.save()
        else:
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
