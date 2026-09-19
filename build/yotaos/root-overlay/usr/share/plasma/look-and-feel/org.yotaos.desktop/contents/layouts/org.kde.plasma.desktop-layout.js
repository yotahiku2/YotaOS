var panel = new Panel
var panelScreen = panel.screen

// YotaOS 0.2 default panel
panel.location = "bottom"
panel.alignment = "center"

// YotaOS panel behavior
panel.lengthMode = "custom"
panel.opacityMode = "adaptive"
panel.floating = true
panel.floatingApplets = true

// 48 px with the standard 18 px Plasma grid unit.
panel.height = gridUnit * (8 / 3)

// Custom centered width: approximately 67% of the display.
const geo = screenGeometry(panelScreen)
const yotaPanelWidth = Math.round(geo.width * 0.672)

panel.minimumLength = yotaPanelWidth
panel.maximumLength = yotaPanelWidth

// YotaOS panel widgets
var yotaLauncher = panel.addWidget("org.kde.plasma.kickoff")
yotaLauncher.currentConfigGroup = ["General"]
yotaLauncher.writeConfig("icon", "/usr/share/yotaos/branding/yotaos-fox.png")
panel.addWidget("org.kde.plasma.icontasks")
panel.addWidget("org.kde.plasma.marginsseparator")
panel.addWidget("org.kde.plasma.systemtray")
panel.addWidget("org.kde.plasma.digitalclock")
panel.addWidget("org.kde.plasma.showdesktop")

// YotaOS desktop wallpaper
var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    desktopsArray[j].wallpaperPlugin = "org.kde.image";
}
