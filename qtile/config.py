import os
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger  # tail ~/.local/share/qtile/qtile.log


mod = 'mod4'
terminal = 'kitty'
using_spacer = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


wallpaper = dict(
    wallpaper='/home/jon/Imagens/jorge-jacinto-azeroth-journey-ironforge.jpg',
    wallpaper_mode='fill',
)


keys = [
    Key([mod], 'Print', lazy.spawn('flatpak run org.flameshot.Flameshot gui')),
    Key([mod], 'space', lazy.widget['keyboardlayout'].next_keyboard()),
    Key([mod], 'r', lazy.spawn('xfce4-appfinder')),
    Key([mod], 'e', lazy.spawn('flatpak run org.mozilla.firefox')),
    Key([mod], 'f', lazy.spawn('thunar')),
    Key([mod], 'p', lazy.spawn('arandr')),
    Key([mod], 'c', lazy.spawn('code')),

    Key([mod], 'h', lazy.layout.left(), desc='Move focus to left'),
    Key([mod], 'l', lazy.layout.right(), desc='Move focus to right'),
    Key([mod], 'j', lazy.layout.down(), desc='Move focus down'),
    Key([mod], 'k', lazy.layout.up(), desc='Move focus up'),

    Key([mod, 'shift'], 'h', lazy.layout.shuffle_left(),
        desc='Move window to the left'),
    Key([mod, 'shift'], 'l', lazy.layout.shuffle_right(),
        desc='Move window to the right'),
    Key([mod, 'shift'], 'j', lazy.layout.shuffle_down(), desc='Move window down'),
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up(), desc='Move window up'),

    Key([mod, 'control'], 'h', lazy.layout.grow_left(),
        desc='Grow window to the left'),
    Key([mod, 'control'], 'l', lazy.layout.grow_right(),
        desc='Grow window to the right'),
    Key([mod, 'control'], 'j', lazy.layout.grow_down(), desc='Grow window down'),
    Key([mod, 'control'], 'k', lazy.layout.grow_up(), desc='Grow window up'),

    Key([mod], 'n', lazy.layout.normalize(), desc='Reset all window sizes'),

    Key([mod], 'Return', lazy.spawn(terminal), desc='Launch terminal'),

    Key([mod], 'Tab', lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod], 'w', lazy.window.kill(), desc='Kill focused window'),

    Key([mod], 't', lazy.window.toggle_floating(),
        desc='Toggle floating on the focused window'),

    Key([mod, 'control'], 'r', lazy.reload_config(), desc='Reload the config'),
]


mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front()),
]


private_group_names = ['󰌾']


def is_private_group(qtile, group_name):
    has_multiple_screens = len(qtile.screens) > 1
    if not has_multiple_screens:
        return False
    is_to_private_group = group_name in private_group_names
    is_second_screen = qtile.current_screen.index == 1
    if is_to_private_group and not is_second_screen:
        return True
    is_private_current_group = qtile.current_group.name in private_group_names
    has_screen_in_group = qtile.groups_map[group_name].screen is not None
    return is_second_screen and is_private_current_group and has_screen_in_group


@lazy.function
def move_to_group(qtile, group_name):
    if is_private_group(qtile, group_name):
        return
    qtile.groups_map[group_name].toscreen()


@lazy.function
def move_window_to_group(qtile, group_name):
    switch_group = not is_private_group(qtile, group_name)
    qtile.current_window.togroup(group_name, switch_group=switch_group)


group_names = ['', '󰅬', '', ''] + private_group_names
groups = [Group(i) for i in group_names]
for i, g in enumerate(groups):
    keys.extend(
        [
            Key(
                [mod],
                f'{i+1}',
                move_to_group(g.name),
                desc=f'Switch to group {g.name}',
            ),
            Key(
                [mod, 'shift'],
                f'{i+1}',
                move_window_to_group(g.name),
                desc='Switch to & move focused window to group {g.name}',
            ),
        ]
    )


mocha_colors = dict(
    Rosewater='#f5e0dc',
    Flamingo='#f2cdcd',
    Pink='#f5c2e7',
    Mauve='#cba6f7',
    Red='#f38ba8',
    Maroon='#eba0ac',
    Peach='#fab387',
    Yellow='#f9e2af',
    Green='#a6e3a1',
    Teal='#94e2d5',
    Sky='#89dceb',
    Sapphire='#74c7ec',
    Blue='#89b4fa',
    Lavender='#b4befe',
    Text='#cdd6f4',
    Subtext1='#bac2de',
    Subtext0='#a6adc8',
    Overlay2='#9399b2',
    Overlay1='#7f849c',
    Overlay0='#6c7086',
    Surface2='#585b70',
    Surface1='#45475a',
    Surface0='#313244',
    Base='#1e1e2e',
    Mantle='#181825',
    Crust='#11111b',
)


layout_theme = dict(
    border_focus=mocha_colors['Teal'],
    border_normal=mocha_colors['Mantle'],
    border_width=3,
    margin=[6, 6, 0, 0],
    margin_on_single=[6, 6, 0, 0],
    border_on_single=True,
)
layouts = [
    layout.Columns(**layout_theme, name='col'),
    layout.Max(**layout_theme),
]


icon_fonts = ['NotoSerif Nerd Font']
text_fonts = ['Ubuntu Nerd Font', 'Cousine Nerd Font']
text_style = {
    'fmt': '<b>{}</b>',
    'font': text_fonts[0]
}


widget_defaults = dict(
    font=text_fonts[0],
    fontsize=12,
    padding=3,
    foreground=mocha_colors['Text'],
    background=mocha_colors['Mantle'],
)
extension_defaults = widget_defaults.copy()


dot = widget.TextBox(
    text='',
    foreground=mocha_colors['Surface0'],
    padding=6
)


screens = [
    Screen(
        **wallpaper,
        top=bar.Bar(
            [
                widget.TextBox(
                    mouse_callbacks={'Button1': lazy.spawn('xfce4-appfinder')},
                    text='',
                    foreground=mocha_colors['Base'],
                    background=mocha_colors['Teal'],
                    padding=9,
                ),
                widget.CurrentLayout(
                    font=text_fonts[1],
                    fmt='<b>{}</b>',
                    foreground=mocha_colors['Base'],
                    background=mocha_colors['Sapphire'],
                    padding=6,
                ),
                widget.GroupBox(
                    highlight_method='line',
                    highlight_color=[
                        mocha_colors['Crust'], mocha_colors['Crust']],
                    background=mocha_colors['Crust'],
                    active=mocha_colors['Lavender'],
                    inactive=mocha_colors['Surface2'],
                    this_current_screen_border=mocha_colors['Lavender'],
                    other_current_screen_border=mocha_colors['Lavender'],
                    this_screen_border=mocha_colors['Surface2'],
                    other_screen_border=mocha_colors['Surface2'],
                    padding=6,
                    use_mouse_wheel=False,
                ),
                widget.Spacer() if using_spacer else dot,
                widget.TextBox(
                    text='󰮂',
                    foreground=mocha_colors['Maroon'],
                ),
                widget.NvidiaSensors(
                    **text_style,
                    format='{perf} {temp}°C',
                    foreground=mocha_colors['Maroon'],
                ),
                dot,
                widget.TextBox(
                    text='',
                    foreground=mocha_colors['Yellow'],
                ),
                widget.CPU(
                    **text_style,
                    format='{load_percent}%',
                    foreground=mocha_colors['Yellow'],
                ),
                widget.ThermalSensor(
                    **text_style,
                    # format='{load_percent}%',
                    foreground=mocha_colors['Yellow'],
                ),
                dot,
                widget.TextBox(
                    text='',
                    foreground=mocha_colors['Teal'],
                ),
                widget.Memory(
                    **text_style,
                    foreground=mocha_colors['Teal'],
                    measure_mem='G',
                    format='{MemUsed: .1f}/{MemTotal: .1f}'
                ),
                widget.Spacer() if using_spacer else dot,
                widget.Systray(padding=6),
                dot,
                widget.TextBox(
                    text='󰕾',
                    foreground=mocha_colors['Sapphire'],
                ),
                widget.Volume(
                    **text_style,
                    foreground=mocha_colors['Sapphire'],
                    mouse_callbacks={'Button1': lazy.spawn('pavucontrol')},
                ),
                dot,
                widget.TextBox(
                    text=' ',
                    foreground=mocha_colors['Sky'],
                ),
                widget.Battery(
                    **text_style,
                    format='{percent:2.0%}{char}',
                    full_char='',
                    # charge_char='',
                    # discharge_char='',
                    # unknown_char='',
                    # empty_char='',
                    not_charging_char='',
                    show_short_text=False,
                    foreground=mocha_colors['Sky'],
                ),
                dot,
                widget.TextBox(
                    text='',
                    foreground=mocha_colors['Lavender'],
                ),
                widget.Clock(
                    **text_style,
                    format='%H:%M',
                    foreground=mocha_colors['Lavender'],
                ),
                dot,
                widget.TextBox(
                    text='',
                    foreground=mocha_colors['Flamingo'],
                ),
                widget.Clock(
                    **text_style,
                    format='%a %d %b',
                    foreground=mocha_colors['Flamingo'],
                ),
                dot,
                widget.TextBox(
                    text='',
                    foreground=mocha_colors['Pink'],
                ),
                widget.KeyboardLayout(
                    **text_style,
                    configured_keyboards=['us intl', 'br'],
                    display_map={'us intl': 'us', 'br': 'br'},
                    foreground=mocha_colors['Pink'],
                ),
                dot,
                widget.QuickExit(
                    countdown_start=1,
                    default_text='',
                    countdown_format='',
                    foreground=mocha_colors['Red'],
                ),
                dot,

            ],
            27,
            background=mocha_colors['Base'],
            margin=[6, 6, 0, 6],
            opacity=0.95,

        ),
        left=bar.Gap(6),
        bottom=bar.Gap(6)
    ),
    Screen(**wallpaper, left=bar.Gap(6), bottom=bar.Gap(6)),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),

        Match(wm_class='xfce4-appfinder'),
        Match(wm_class='xfce4-notifyd'),
        Match(wm_class='blueman-manager'),
        Match(wm_class='Places'),
        Match(wm_class='pavucontrol')
    ]
)
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = 'smart'
reconfigure_screens = True

wmname = 'LG3D'
