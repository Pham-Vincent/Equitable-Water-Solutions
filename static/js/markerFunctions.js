
export function setMarkerIcon(designatedUse){
    if (designatedUse === "Mining") {
        return "static/images/triangle.png";
    }
    if (designatedUse === "Fire and Hyrdrostatic") {
        return "static/images/hexagon.png";
    }
    if (designatedUse === "Power Related") {
        return "static/images/square.png";
    }
    if (designatedUse === "Institutional Use") {
        return "static/images/circle.png";
    }
    if (designatedUse === "Industrial Use") {
        return "static/images/diamond.png";
    }
    if (designatedUse === "Commercial Use") {
        return "static/images/pentagon.png";
    }
    if (designatedUse === "Other Irrigation") {
        return "static/images/star-2.png";
    }
    if (designatedUse === "Crop Irrigation") {
        return "static/images/star.png";
    }
}