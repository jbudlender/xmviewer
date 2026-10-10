# Xhorha Mouth viewer (beta)

An interactive map of the Xhorha Mouth area (Eastern Cape, South Africa) where
you can flip between aerial photographs from 1942 to 2026 and see how the
landscape has changed.

**Live:** https://www.joshbudlender.co.za/xmviewer/ (also via https://jbudlender.github.io/xmviewer/)

Produced by Joshua Budlender (SALDRU, University of Cape Town) as part of the
Bulungula Incubator Sentinel Site Survey.

## Status

This is a work in progress:

- 1942–2006: temporary low-resolution preview scans; high-resolution scans are
  on their way.
- Greyed-out years (1962, 1963, 1974, 1985, 1996): photos requested, not yet received.
- 2009–2026: temporarily reduced resolution (~1 m); additional map sheets still to arrive.

The historical photos (1942–2006) were georeferenced automatically against the
NGI orthophotos; expect shifts of roughly 5–20 m between years.

## Imagery and credits

All aerial photography and orthophotos: **National Geo-spatial Information
(NGI), South Africa** ([ngi.dalrrd.gov.za](https://ngi.dalrrd.gov.za/)), used with
permission. The imagery is not covered by this repository's licence.

## What's here

| Path | Contents |
|---|---|
| `index.html` | The viewer (Leaflet + PMTiles; desktop and phone layouts) |
| `layers.json` | The list of years: available or not, tile file, maximum zoom |
| `tiles/<year>.pmtiles` | One file of map tiles per year |
| `data/villages.geojson` | Village boundaries |
| `tools/serve.py` | Local preview server |

The tiles are produced from the source imagery by a separate processing
pipeline (not in this repository).

## Preview locally

```bash
python3 tools/serve.py          # then open http://localhost:8000
python3 tools/serve.py --lan    # also reachable from a phone on the same Wi-Fi
```

(`python3 -m http.server` won't work: PMTiles needs HTTP range requests.)

## Licence

Code (`index.html`, `tools/`): MIT — see `LICENSE`. Imagery: © NGI, see above.
