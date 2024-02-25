#!/usr/bin/env sh

dbus-update-activation-environment --all &

gnome-keyring-daemon --start --components=pkcs11,secrets,ssh &

/usr/libexec/polkit-gnome-authentication-agent-1 &

/usr/libexec/xfce4/notifyd/xfce4-notifyd &

picom --config ~/.config/picom/picom.conf &

blueman-applet &

nm-applet &