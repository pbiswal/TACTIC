###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#

__all__ = ['SObjectCheckinWdg', 'SObjectCheckinCbk', 'CheckboxCheckinWdg', 'DescriptionCheckinWdg']


from pyasm.command import *
from pyasm.search import *
from pyasm.web import *
from pyasm.widget import *
from pyasm.prod.biz import *
from prod_wdg import *
from shot_navigator_wdg import *
from pyasm.prod.web import *
from pyasm.prod.checkin import *



class SObjectCheckinException(Exception):
    pass




class SObjectCheckinWdg(Widget):
    '''General SObject snapshot checkin widget'''

    def init(my):
        my.register_cmd()
        my.handle_introspect()
        my.handle_filter()
        my.handle_checkin()

    def handle_filter(my):
        shot_navigator = ShotNavigatorWdg()
        my.add(shot_navigator)



    def register_cmd(my):
        '''register the command that will handle this widget'''
        WebContainer.register_cmd("pyasm.prod.web.SObjectCheckinCbk")



    def handle_checkin(my):

        shot = ProdContext.get_shot()
        if not shot:
            my.add(DivWdg("No shot is defined"))
            return
        search = Search("prod/layer")
        search.add_filter("shot_code", shot.get_code() )

        table = TableWdg("prod/layer", "checkin")
        table.set_search(search)

        my.add(table)


    def handle_introspect(my):
        button = IntrospectWdg()
        button.add_style("float", "right")
        my.add(button)
    
    




class SObjectCheckinCbk(Command):

    def get_title(my):
        return "SObject Checkin"

    def execute(my):
        web = WebContainer.get_web()
        if web.get_form_value(CheckboxCheckinWdg.PUBLISH_BUTTON) != "":
            search_key = web.get_form_value("search_key")
            if search_key == "":
                return CommandExitException()

            sobject = Search.get_by_search_key(search_key)

            # use the group checkin
            # TODO: convert this to using snapshot types!!!
            sobject_checkin = MayaSObjectCheckin(sobject)
            sobject_checkin.execute()

            my.description = "Checkin in sobject [%s]" % sobject.get_code()

        else:
            return CommandExitException()


               




class CheckboxCheckinWdg(BaseTableElementWdg):

    PUBLISH_BUTTON = "Publish"
    def get_title(my):
        button = IconSubmitWdg(my.PUBLISH_BUTTON, long=True)
        button.add_style("height: 14px")
        button.add_style("padding: 3px 10px 3px 10px")
        button.set_attr("onclick", "return checkin_selected_sobjects()")
        return button


    def get_display(my):
        sobject = my.get_current_sobject()

        search_key = sobject.get_search_key()

        checkbox = CheckboxWdg("search_key")
        checkbox.set_option("value", search_key)
        return checkbox




class DescriptionCheckinWdg(BaseTableElementWdg):

    def get_display(my):

        sobject = my.get_current_sobject()
        search_key = sobject.get_search_key()

        textarea = TextAreaWdg()
        textarea.set_name("%s_description" % search_key)
        textarea.set_attr("cols", "25")
        textarea.set_attr("rows", "1")

        return textarea



