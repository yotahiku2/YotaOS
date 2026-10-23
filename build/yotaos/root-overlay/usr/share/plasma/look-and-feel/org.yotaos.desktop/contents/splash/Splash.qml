import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "#080d18"

    property int stage

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true
            foxPulse.running = true
            glowPulse.running = true
        } else if (stage == 5) {
            outroAnimation.running = true
        }
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Rectangle {
            id: glow
            width: fox.width * 1.35
            height: width
            radius: width / 2
            anchors.centerIn: fox
            color: "#1a5fb4"
            opacity: 0.18
            scale: 1.0
        }

        Image {
            id: fox
            readonly property real size: Kirigami.Units.gridUnit * 9

            width: size
            height: size

            anchors.centerIn: parent
            anchors.verticalCenterOffset: -Kirigami.Units.gridUnit * 1.2

            asynchronous: true
            smooth: true
            fillMode: Image.PreserveAspectFit
            source: "images/yotaos-fox.png"
            sourceSize.width: size
            sourceSize.height: size
        }

        Text {
            id: title
            anchors.top: fox.bottom
            anchors.topMargin: Kirigami.Units.gridUnit * 1.2
            anchors.horizontalCenter: parent.horizontalCenter

            text: "YotaOS"
            color: "#eff0f1"
            font.pixelSize: Kirigami.Units.gridUnit * 1.15
            font.weight: Font.DemiBold
        }

        Text {
            id: subtitle
            anchors.top: title.bottom
            anchors.topMargin: Kirigami.Units.smallSpacing
            anchors.horizontalCenter: parent.horizontalCenter

            text: "starting secure workspace..."
            color: "#9fb3c8"
            font.pixelSize: Kirigami.Units.gridUnit * 0.72
        }
    }

    OpacityAnimator {
        id: introAnimation
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }

    OpacityAnimator {
        id: outroAnimation
        target: content
        from: 1
        to: 0
        duration: Kirigami.Units.longDuration
        easing.type: Easing.InOutQuad
    }

    SequentialAnimation {
        id: foxPulse
        loops: Animation.Infinite
        running: false

        NumberAnimation {
            target: fox
            property: "scale"
            from: 1.0
            to: 1.035
            duration: 1400
            easing.type: Easing.InOutQuad
        }

        NumberAnimation {
            target: fox
            property: "scale"
            from: 1.035
            to: 1.0
            duration: 1400
            easing.type: Easing.InOutQuad
        }
    }

    SequentialAnimation {
        id: glowPulse
        loops: Animation.Infinite
        running: false

        ParallelAnimation {
            NumberAnimation {
                target: glow
                property: "scale"
                from: 1.0
                to: 1.12
                duration: 1400
                easing.type: Easing.InOutQuad
            }
            NumberAnimation {
                target: glow
                property: "opacity"
                from: 0.16
                to: 0.28
                duration: 1400
                easing.type: Easing.InOutQuad
            }
        }

        ParallelAnimation {
            NumberAnimation {
                target: glow
                property: "scale"
                from: 1.12
                to: 1.0
                duration: 1400
                easing.type: Easing.InOutQuad
            }
            NumberAnimation {
                target: glow
                property: "opacity"
                from: 0.28
                to: 0.16
                duration: 1400
                easing.type: Easing.InOutQuad
            }
        }
    }
}
