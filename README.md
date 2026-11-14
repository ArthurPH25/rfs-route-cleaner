# RFS Route Cleaner

Cleans KML routes exported from SimBrief so they import properly into
Real Flight Simulator (RFS).

## The problem

When you export a SimBrief route as "Google Earth KML" and import it into RFS,
the route often contains two waypoints with the same name at the same spot.
RFS flies to the first one, sees the second one right on top of it, and makes a
180° turn just to pass over the same point again. In cruise, that is a mess.

This script removes those repeated waypoints from the route line, so the
route runs straight through each point once.

## Requirements

Python 3. Only the standard library is used (tested with Python 3.12).

## How to use

1. Export your flight plan from SimBrief as Google Earth KML.
2. Put the `.kml` file in the same folder as `rfs-route-cleaner.py`.
3. Run the script from a terminal in that folder:

   ```
   python rfs-route-cleaner.py
   ```

   (Running it from a terminal keeps the output on screen. If you
   double-click the script, the window closes as soon as it finishes.)
4. Import the new `CLEAN_<original name>.kml` file from the `cleaned` folder in RFS.

Every `.kml` file in the script's folder is processed in one run, so you can
clean several routes at once. Your original files are never changed.

The cleaned files are written to a `cleaned` folder next to the script, which
is created on the first run. Only the script's own folder is scanned for
input, so running it again never picks up its own output.

## What it does to the file

Only the `Route` line is rewritten: it is rebuilt from the waypoint points in
the file, in their original order, dropping any point that has the same
coordinates as the one right before it. Everything else in the file stays as
it was.

If you run the script again for the same source file, the existing file in
`cleaned` is overwritten.

## Messages

- `[SUCCESS]` the cleaned file was written.
- `[ERROR] Route element not found` the file has no placemark named `Route`
  (or it is not a KML 2.2 file). Make sure it is the SimBrief Google Earth KML.
- `[ERROR] Fewer than 2 waypoints found` the file has no usable waypoint
  points, so no output was written.
- `[ERROR] Failed to process` the file could not be read or written, for
  example because it is not valid XML.
