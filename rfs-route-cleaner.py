import xml.etree.ElementTree as ET
from pathlib import Path


KML_NAMESPACE = "http://www.opengis.net/kml/2.2"
NAMESPACES = {"kml": KML_NAMESPACE}
OUTPUT_PREFIX = "CLEAN_"
OUTPUT_FOLDER = "cleaned"


def clean_kml_file(file_path: Path) -> bool:
    ET.register_namespace("", KML_NAMESPACE)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        waypoint_coordinates = []

        for placemark in root.findall(".//kml:Placemark", NAMESPACES):
            name = placemark.find("kml:name", NAMESPACES)
            point = placemark.find(".//kml:Point/kml:coordinates", NAMESPACES)

            if name is None or point is None or name.text == "Route":
                continue

            coordinate = (point.text or "").strip()

            if coordinate and (
                not waypoint_coordinates or waypoint_coordinates[-1] != coordinate
            ):
                waypoint_coordinates.append(coordinate)

        route_coordinates = root.find(
            './/kml:Placemark[kml:name="Route"]//kml:coordinates',
            NAMESPACES,
        )

        if route_coordinates is None:
            print(f"[ERROR] Route element not found: {file_path.name}")
            return False

        if len(waypoint_coordinates) < 2:
            print(
                f"[ERROR] Fewer than 2 waypoints found, file skipped: "
                f"{file_path.name}"
            )
            return False

        route_coordinates.text = "\n" + "\n".join(waypoint_coordinates) + "\n"

        output_directory = file_path.parent / OUTPUT_FOLDER
        output_directory.mkdir(exist_ok=True)
        output_path = output_directory / f"{OUTPUT_PREFIX}{file_path.name}"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        print(
            f"[SUCCESS] {file_path.name} -> {OUTPUT_FOLDER}/{output_path.name} "
            f"({len(waypoint_coordinates)} waypoints)"
        )
        return True

    except Exception as error:
        print(f"[ERROR] Failed to process {file_path.name}: {error}")
        return False


def main() -> None:
    script_directory = Path(__file__).resolve().parent

    kml_files = sorted(
        file_path
        for file_path in script_directory.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() == ".kml"
    )

    if not kml_files:
        print(f"No KML files found in: {script_directory}")
        return

    print(f"Found {len(kml_files)} KML file(s). Starting processing...\n")

    successful = 0
    failed = 0

    for file_path in kml_files:
        if clean_kml_file(file_path):
            successful += 1
        else:
            failed += 1

    print(f"\nProcessing completed: {successful} successful, {failed} failed.")


if __name__ == "__main__":
    main()
