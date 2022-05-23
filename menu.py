#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame_menu
from constants import WIDTH, HEIGHT



class Menu:
    def __init__(self, run_simulation_cb, reset_cb, set_population_cb, set_steps_cb, set_mutation_rate_cb):
        self._theme = pygame_menu.Theme(
            background_color=pygame_menu.themes.THEME_DARK.background_color,
            title=False,
            widget_font=pygame_menu.font.FONT_FIRACODE,
            widget_font_color=(255, 255, 255),
            widget_margin=(0, 15),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )

        self._menu = pygame_menu.Menu(
            height=HEIGHT,
            mouse_motion_selection=True,
            position=(WIDTH-240, 0, False),
            theme=self._theme,
            title='',
            width=240
        )

        self._menu.add.label(
            'Mutation Chance',
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=19,
            margin=(0, 5)
        )

        txt_input = self._menu.add.text_input(
            '',
            default=0.01,
            maxchar=6,
            maxwidth=7,
            onchange=set_mutation_rate_cb,
            textinput_id='mutation_rate',
            input_type=pygame_menu.locals.INPUT_FLOAT,
            cursor_selection_enable=False
        )

        txt_input.set_background_color((75, 79, 81))


        self._menu.add.label(
            'Max Steps',
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=19,
            margin=(0, 5)
        )

        txt_input = self._menu.add.text_input(
            '',
            default=400,
            maxchar=4,
            maxwidth=5,
            onchange=set_steps_cb,
            textinput_id='steps',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        )

        txt_input.set_background_color((75, 79, 81))



        self._menu.add.label(
            'Population',
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=19,
            margin=(0, 5)
        )

        txt_input = self._menu.add.text_input(
            '',
            default=1000,
            maxchar=4,
            maxwidth=5,
            onchange=set_population_cb,
            textinput_id='population',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        )

        txt_input.set_background_color((75, 79, 81))

        self._menu.add.vertical_margin(10)

        #btn = self._menu.add.button(
        #    'Restart Run Simulation',
        #    run_simulation_cb,
        #    button_id="run_simulation",
        #    font_size=20,
        #    margin=(0, 30),
        #    shadow_width=10
        #)

        #btn.set_onmouseover(Menu._button_onmouseover)
        #btn.set_onmouseleave(Menu._button_onmouseleave)
        #btn.set_background_color((75, 79, 81))

        #self._menu.add.vertical_margin(10)

        btn = self._menu.add.button(
            'Apply And Restart',
            reset_cb,
            button_id="reset",
            font_size=20,
            margin=(0, 30),
            shadow_width=10
        )

        btn.set_onmouseover(Menu._button_onmouseover)
        btn.set_onmouseleave(Menu._button_onmouseleave)
        btn.set_background_color((75, 79, 81))



    def _button_onmouseover(w: 'pygame_menu.widgets.Widget', _):
        w.set_background_color((98, 103, 106))


    def _button_onmouseleave(w: 'pygame_menu.widgets.Widget', _):
        w.set_background_color((75, 79, 81))


    def get_menu(self):
        return self._menu
