from flet import *
import flet as ft

import random

def main(page: ft.Page):

    '''
    allign
    '''
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    '''
    Container
    '''
    c1 = ft.Container(
        ft.Text("A", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.alignment.center,
        width=100,
        height=100,
        bgcolor=ft.colors.GREEN,
    )
    c2 = ft.Container(
        ft.Text("B", size=50),
        alignment=ft.alignment.center,
        width=100,
        height=100,
        bgcolor=ft.colors.YELLOW,
    )

    '''
    Container Switch
    '''
    c = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        offset = transform.Offset(0,0),
    )

    '''
    Animation
    '''
    def animate(e):
        c.content = c2 if c.content == c1 else c1
        c.offset = transform.Offset(random.randrange(-1, 2), random.randrange(-1, 2)) if c.offset == transform.Offset(0, 0) else transform.Offset(0, 0)
        c.update()

    '''
    ADD
    '''
    page.add(
        c,
        ft.ElevatedButton("Click!", on_click=animate, offset=transform.Offset(0,4)),
    )


ft.app(target=main)