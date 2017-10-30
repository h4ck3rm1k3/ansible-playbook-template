#!/usr/bin/python
import sys



sys.path.append("/home/mdupont/experiments/ansible/ansible/lib")
import ansible.modules.files.file as filemodule
import ansible.modules.files.template as templatemodule
from ansible.module_utils import basic
import ansible.vars
import ansible.template
from ansible.template import Templar
from jinja2.loaders import FileSystemLoader
from ansible.template import generate_ansible_template_vars

            
import json

def domodule(m, args):
    basic._ANSIBLE_ARGS = json.dumps(dict(
        ANSIBLE_MODULE_ARGS=args
    ))
    m.main()
    
def dofile(args): 
    domodule(filemodule,args)


playbooks = [
    'public-server',
    'laptop',
    'phone',
    'internal-server',
]

class Playbook(object):
    def __init__(self,name):
        self.name = name

    def site_yaml(self):
        pass
    def hosts(self):
        pass
    

# name

print "helo"
#filemodule.

if False:
    dofile({
    'path': "playbook",
    'state': 'directory'
    })




class MyLoader:
    def get_basedir(self):
        return "."
    def path_dwim_relative_stack(self, path_stack, dirname, needle):
        return ""


def dotemplate(args): 
    domodule(templatemodule,args)
#from ansible.playbook.attribute import FieldAttribute
import ansible.plugins.action.template as atemplate

class TemplateTask():
    def __init__(self, src, dest,task_vars={}):
        self.async = False          
        self.src = src
        self.dest = dest
        self.force = False
        self.state = None
#        self.args = Args(self)
        self.environment = ""
        #        self._templar = Templatar(templar)
        self._loader = MyLoader()
        self._templar = Templar(self._loader)
        self.task_vars=task_vars
    def get_search_path(self):
        return ""
    #@property
    #def args(self)
    #    return 
    def run(self):

        #source = "fake"
        data = "".join(open(self.src).readlines())
        
        # add ansible 'template' vars
        temp_vars = self.task_vars.copy()
        temp_vars.update(generate_ansible_template_vars(self.src))

        old_vars = self._templar._available_variables
        self._templar.set_available_variables(temp_vars)

        resultant = self._templar.do_template(data, preserve_trailing_newlines=True, escape_backslashes=False)
        self._templar.set_available_variables(old_vars)

        o = open(self.dest,"w")
        o.write(resultant)
        o.close()
        
        return resultant

roles =  {
    'common' : {

    },
    'webtier' : {

    }
}

aspects = {
    'aspect1' : {
        'hosts' : 'all',
        'roles' : [
            'common',
            'webtier'
        ]
    },
    'aspect2' : {
        'hosts' : 'all',
        'roles' : [
            'common',
            'webtier'
        ]
    }
}

import yaml

task = TemplateTask(
    src='templates/site.yml',
    dest="playbook/site.yml",
    task_vars = {
        "aspect_names" : aspects.keys()
    })
r = task.run()
for a in aspects:
    o = aspects[a]
    task = TemplateTask(
        src='templates/aspect.yml',
        dest="playbook/{}.yml".format(a),
        task_vars = {
            "hosts" : o['hosts'],
            "roles" : o['roles']
    })
    r = task.run()

import os
rb = "playbook/roles/"
if not os.path.exists(rb):
    os.mkdir(rb)

for a in roles:
    o = roles[a]
    r = "playbook/roles/{}/".format(a)
    if not os.path.exists(r):
        os.mkdir(r)

    task = TemplateTask(
        src='templates/role.yml',
        dest=r + "main.yml",
        task_vars = {
        })
    r = task.run()

hosts = {
    'all' : {
        'hosts' : {
            'host1' : {},
            'host2' : {},
            
        },
        'vars' :  {
            'dhcp_server' :  'foo'
        }         
    }
}

group_vars = {
    'all' : {}
}

host_vars = {
    'host1' : {
        'ansible_connection':'local',
        'ansible_host' :  'localhost',
    },
    'host2' : {
        'ansible_connection':'local',
        'ansible_host' :  'localhost',
    }
}

task = TemplateTask(
    src='templates/hosts.yml',
    dest="playbook/hosts.yml",
    task_vars = {
        "hosts" : yaml.dump(hosts)
    })
r = task.run()

r = "playbook/group_vars/"
if not os.path.exists(r):
    os.mkdir(r)

r = "playbook/host_vars/"
if not os.path.exists(r):
    os.mkdir(r)

for g in group_vars:
    task_vars = yaml.dump(group_vars[g])
    task = TemplateTask(
        src='templates/group_vars.yml',
        dest="playbook/group_vars/{}".format(g),
        task_vars = {'group_vars':task_vars},
    )
    r = task.run()

for g in host_vars:
    task = TemplateTask(
        src='templates/host_vars.yml',
        dest="playbook/host_vars/{}".format(g),
        task_vars = {'host_vars':yaml.dump(host_vars[g])})
    r = task.run()

task = TemplateTask(
    src='templates/ansible.cfg',
    dest="playbook/ansible.cfg",
    task_vars = {    })
r = task.run()


# production                # inventory file for production servers
# staging                   # inventory file for staging environment

# group_vars/
#    group1                 # here we assign variables to particular groups
#    group2                 # ""
# host_vars/
#    hostname1              # if systems need specific variables, put them here
#    hostname2              # ""

# library/                  # if any custom modules, put them here (optional)
# module_utils/             # if any custom module_utils to support modules, put them here (optional)
# filter_plugins/           # if any custom filter plugins, put them here (optional)

# site.yml                  # master playbook
# webservers.yml            # playbook for webserver tier
# dbservers.yml             # playbook for dbserver tier

# roles/
#     common/               # this hierarchy represents a "role"
#         tasks/            #
#             main.yml      #  <-- tasks file can include smaller files if warranted
#         handlers/         #
#             main.yml      #  <-- handlers file
#         templates/        #  <-- files for use with the template resource
#             ntp.conf.j2   #  <------- templates end in .j2
#         files/            #
#             bar.txt       #  <-- files for use with the copy resource
#             foo.sh        #  <-- script files for use with the script resource
#         vars/             #
#             main.yml      #  <-- variables associated with this role
#         defaults/         #
#             main.yml      #  <-- default lower priority variables for this role
#         meta/             #
#             main.yml      #  <-- role dependencies
#         library/          # roles can also include custom modules
#         module_utils/     # roles can also include custom module_utils
#         lookup_plugins/   # or other types of plugins, like lookup in this case

#     webtier/              # same kind of structure as "common" was above, done for the webtier role
#     monitoring/           # ""
#     fooapp/               # ""
    

#setattr(task,'args',args)

import pprint


#print r

#source = 
#template_data="foo"
#print t.doit(task_vars, source, template_data)

#pprint.pprint(r)

# dotemplate({ # master playbook
#     'src' : ,
#     'dest': ,
#     'contents' : [ { 'include' : x + "yaml"} for x in playbooks ] 
# })

