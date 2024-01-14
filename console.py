#!/usr/bin/python3
"""Defines the AirBnB console (hbnb). """

import cmd
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Defines the AirBnB command interpreter.

    Atrributes:
        promt(str): command promt.
    """

    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Place", "State", "City", "Amenity", "Review"]

    def empty_line(self):
        """Do nothing when receiving an empty line."""
        pass
    def do_quit(self, arg):
        """Quit command to exit program."""
        return True

    def help_quit(self, arg):
        """Defines the action of the quit command """
        print("Quit command to exit program")

    def do_EOF(self, arg):
        """EOF signal for exiting the program."""
        print()
        return True

    def do_create(self, arg):
        """Creates an instance of the BaseModel and save it to JSON file.
                Usage: create <class>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Shows the str representation of an instance
            Usage: show <class> <id>
        """

        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
         Deletes an instance based on the class name and id 
            then saves the change into the JSON file.
                Usage: destroy <class> <id>
        """

        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints str representation of instances based on the class name or not.
            Usage: all or all <class>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            objects = storage.all()
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id.
        Adds or updates attribute and saves change to JSON file.
            Usage: update <class name> <id> <attribute name> "<attribute value>"
        """

        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])

            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                attr_name = commands[2]
                attr_value = commands[3]

                try:
                    attr_value = eval(attr_value)
                except Exception:
                    pass

                setattr(obj, attr_name, attr_value)
                obj.save()

    def default(self, arg):
        """Reprogram default behavior for cmd module when input is invalid."""
        arg_list = arg.split('.')
        cls_name = arg_list[0]
        command = arg_list[1].split('(')
        method_name = command[0]
        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update
        }
        
        if method_name in method_dict.keys():
            return method_dict[method_name]("{}.{}".format(cls_name, ''))

        print("*** Unknown syntax: {}".format(arg))
        return False




if __name__ == "__main__":
    HBNBCommand().cmdloop()
