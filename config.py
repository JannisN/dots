# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "s", lazy.next_screen(), desc="Switch monitors"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn('kitty'), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.spawn('rofi -show run'), desc="Rofi start"),
    Key([], "XF86MonBrightnessUp", lazy.spawn('brightnessctl s 16+'), desc="Rofi start"),
    Key([], "XF86MonBrightnessDown", lazy.spawn('brightnessctl s 16-'), desc="Rofi start"),
    Key([mod], "e", lazy.spawn('thunar'), desc="Thunar start"),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "a", lazy.window.toggle_fullscreen()),
]

groups = [Group(name=i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#00ffff", "#8f3d3d"], border_width=0, margin=0, border_focus="#ffaaaa", border_normal="#66aaff"),
    #layout.Columns(border_focus_stack=["#00ffff", "#8f3d3d"], border_width=0, padding=0, border_focus="#66aaff", border_normal="#222222"),
    #layout.Max(),
    layout.Floating(border_width=0, margin=3, border_focus="#ffaaaa", border_normal="#66aaff"),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(border_width=0, margin=10, border_focus="#ffaaaa", border_normal="#66aaff"),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Fira Mono Nerd Font",
    fontsize=12,
    padding=3,
    foreground='ffffff',
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.TextBox("", name="default", font="Fira Mono Nerd Font", fontsize=23, padding=16, mouse_callbacks={'Button1': lazy.spawn('rofi -show run')}),
                widget.TextBox("󰣇", name="default", font="Fira Mono Nerd Font", fontsize=26, padding=16, mouse_callbacks={'Button1': lazy.spawn('rofi -show run')}),
                widget.Prompt(fontsize=16, font="Fira Mono Nerd Font"),
                #widget.Mpd2(),
                #widget.Mpris2(
                #    objname='org.mpris.MediaPlayer2.spotify',
                #    name='spotify',
                    #objname="org.mpris.MediaPlayer2.spotify",
                    #display_metadata=['xesam:title', 'xesam:artist'],
                    #scroll_chars=None,
                    #stop_pause_text='asdf',
                #),
                widget.Spacer(),
                #widget.GroupBox(fontsize=18, disable_drag=True, hide_unused=True, highlight_method='line', padding_y=7, padding_x=7, margin_x=0, font="FuraMono Nerd Font Mono", inactive="333333", this_current_screen_border="3175a8aa", this_screen_border="3175a8aa", other_current_screen_border="333333aa", other_screen_border="333333aa", active="333333ff", highlight_color=["ffffff00","ffffff00"], rounded=False),
                widget.GroupBox(fontsize=18, disable_drag=True, hide_unused=True, highlight_method='text', padding_y=0, padding_x=2, margin_x=0, font="Fira Mono Nerd Font", inactive="3a3a3a", this_current_screen_border="ffffff", this_screen_border="aaaaaa", active="999999", block_highlight_text_color="333333dd", foreground="404040"),
                #widget.WindowName(),
                #widget.CPU(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Spacer(hci="/dev_FD_77_CC_74_A1_ED"),
                #widget.Systray(),
                #widget.TextBox("default configfIconIconIcoIconnIcon", name="default", font="FuraMono Nerd Font Mono"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                #widget.Systray(),
                #widget.CurrentLayoutIcon(markup=True, scale=0.5, fontsize=16, padding=10, font="Fira Mono Nerd Font"),
                widget.CurrentLayout(markup=True, fontsize=16, padding=10, font="Fira Mono Nerd Font"),
                widget.TextBox(" ", fontsize=3),
                widget.TextBox("󰂯", name="default", font="Fira Mono Nerd Font", fontsize=20, padding=4, mouse_callbacks={'Button1': lazy.spawn('blueman-manager')}),
                widget.TextBox("", name="default", font="Fira Mono Nerd Font", fontsize=22, padding=10, mouse_callbacks={'Button1': lazy.spawn('kitty')}),
                widget.TextBox("", name="default", font="Fira Mono Nerd Font", fontsize=20, padding=10, mouse_callbacks={'Button1': lazy.spawn('thunar')}),
                widget.TextBox("", name="default", font="Fira Mono Nerd Font", fontsize=20, padding=10, mouse_callbacks={'Button1': lazy.spawn('pavucontrol')}),
                widget.TextBox("", name="default", font="Fira Mono Nerd Font", fontsize=15, padding=10, mouse_callbacks={'Button1': lazy.spawn('firefox')}),
                widget.TextBox(" "),
                widget.Wlan(interface="wlp1s0", disconnected_message="", format=" ", fontsize=18, mouse_callbacks={'Button1': lazy.spawn('nm-connection-editor')}),
                widget.Wlan(interface="wlp1s0", format="{essid}", fontsize=16, mouse_callbacks={'Button1': lazy.spawn('nm-connection-editor')}),
                widget.TextBox("  ", fontsize=4),
                widget.Battery(show_short_text=False, full_char='󰂄', empty_char='󰁺', charge_char='󰂈', discharge_char='󰁿', format='{char}', font="Fira Mono Nerd Font", fontsize=17, padding=8),
                widget.Battery(format='{percent:2.0%}', font="Fira Mono Nerd Font", fontsize=16),
                widget.Clock(format="%a. %d. %b. %H:%M", fontsize=16, padding=20, font="Fira Mono Nerd Font"),
                #widget.QuickExit(),
            ],
            32,
            margin=[0, 0, 0, 0],
            background='#202127'
            #background='#101117cb'
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        left=bar.Gap(0),
        right=bar.Gap(0),
        bottom=bar.Gap(0)
    ),
    Screen(
        top=bar.Bar(
            [
                widget.TextBox("", name="default", font="FuraMono Nerd Font Mono", fontsize=36, padding=16, mouse_callbacks={'Button1': lazy.spawn('rofi -show run')}),
                widget.Prompt(fontsize=16, font="FuraMono Nerd Font Mono"),
                #widget.Mpd2(),
                #widget.Mpris2(
                #    objname='org.mpris.MediaPlayer2.spotify',
                #    name='spotify',
                    #objname="org.mpris.MediaPlayer2.spotify",
                    #display_metadata=['xesam:title', 'xesam:artist'],
                    #scroll_chars=None,
                    #stop_pause_text='asdf',
                #),
                widget.Spacer(),
                widget.GroupBox(fontsize=18, disable_drag=True, hide_unused=True, highlight_method='block', padding_y=7, padding_x=9, margin_x=-3, font="FuraMono Nerd Font Mono", inactive="333333", this_current_screen_border="3175a8aa", this_screen_border="3175a8aa", active="333333", block_highlight_text_color="ffffff"),
                #widget.GroupBox(fontsize=18, disable_drag=True, hide_unused=True, highlight_method='line', padding_y=7, padding_x=7, margin_x=0, font="FuraMono Nerd Font Mono", inactive="333333", this_current_screen_border="3175a8aa", this_screen_border="3175a8aa", other_current_screen_border="333333aa", other_screen_border="333333aa", active="333333ff", highlight_color=["ffffff00","ffffff00"], rounded=False),
                #widget.GroupBox(fontsize=18, disable_drag=True, hide_unused=True, highlight_method='block', padding_y=7, padding_x=9, margin_x=-3, font="FuraMono Nerd Font Mono", inactive="ffffff", this_current_screen_border="3175a8aa", this_screen_border="3175a8aa"),
                #widget.WindowName(),
                #widget.CPU(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Spacer(),
                #widget.Systray(),
                #widget.TextBox("default configfIconIconIcoIconnIcon", name="default", font="FuraMono Nerd Font Mono"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                #widget.Systray(),
                widget.CurrentLayout(markup=True, fontsize=16, padding=20, font="FuraMono Nerd Font"),
                widget.TextBox("", name="default", font="FuraMono Nerd Font Mono", fontsize=18, padding=10, mouse_callbacks={'Button1': lazy.spawn('blueman-manager')}),
                widget.TextBox("", name="default", font="FuraMono Nerd Font Mono", fontsize=26, padding=10, mouse_callbacks={'Button1': lazy.spawn('kitty')}),
                widget.TextBox("", name="default", font="FuraMono Nerd Font Mono", fontsize=26, padding=10, mouse_callbacks={'Button1': lazy.spawn('thunar')}),
                widget.TextBox("墳", name="default", font="FuraMono Nerd Font Mono", fontsize=26, padding=10, mouse_callbacks={'Button1': lazy.spawn('pavucontrol')}),
                widget.TextBox("", name="default", font="FuraMono Nerd Font Mono", fontsize=26, padding=10, mouse_callbacks={'Button1': lazy.spawn('firefox')}),
                widget.Clock(format="%a. %d. %b. %H:%M", fontsize=16, padding=20, font="FuraMono Nerd Font"),
                #widget.QuickExit(),
            ],
            32,
            margin=[0, 0, 10, 0],
            background='#ffffffe6'
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        left=bar.Gap(4),
        right=bar.Gap(4),
        bottom=bar.Gap(4)
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_width=0, margin=10, border_focus="#ffaaaa", border_normal="#66aaff", #border_width = 0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])
