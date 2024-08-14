var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc2) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc2 = __getOwnPropDesc(from, key)) || desc2.enumerable });
  }
  return to;
};
var __reExport = (target, mod, secondTarget) => (__copyProps(target, mod, "default"), secondTarget && __copyProps(secondTarget, mod, "default"));

// lib/widget.ts
import * as mc from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { Query as Query5 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as arrow3 from "https://esm.sh/apache-arrow@16.1.0";
import * as uuid from "https://esm.sh/@lukeed/uuid@2.0.1";
import { effect as effect5 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/clients/DataTable.ts
import * as arrow2 from "https://esm.sh/apache-arrow@16.1.0";
import {
  MosaicClient as MosaicClient4,
  Selection as Selection2
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { desc, Query as Query4 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as signals from "https://esm.sh/@preact/signals-core@1.6.1";
import { html } from "https://esm.sh/htl@0.3.1";

// lib/utils/assert.ts
var AssertionError = class extends Error {
  /** @param message The error message. */
  constructor(message) {
    super(message);
    this.name = "AssertionError";
  }
};
function assert(expr, msg = "") {
  if (!expr) {
    throw new AssertionError(msg);
  }
}

// lib/utils/AsyncBatchReader.ts
var AsyncBatchReader = class {
  /** the iterable batches to read */
  #batches = [];
  /** the index of the current row */
  #index = 0;
  /** resolves a promise for when the next batch is available */
  #resolve = null;
  /** the current batch */
  #current = null;
  /** A function to request more data. */
  #requestNextBatch;
  /**
   * @param requestNextBatch - a function to request more data. When
   * this function completes, it should enqueue the next batch, otherwise the
   * reader will be stuck.
   */
  constructor(requestNextBatch) {
    this.#requestNextBatch = requestNextBatch;
  }
  /**
   * Enqueue a batch of data
   *
   * The last batch should have `last: true` set,
   * so the reader can terminate when it has
   * exhausted all the data.
   *
   * @param batch - the batch of data to enqueue
   * @param options
   * @param options.last - whether this is the last batch
   */
  enqueueBatch(batch, { last }) {
    this.#batches.push({ data: batch, last });
    if (this.#resolve) {
      this.#resolve();
      this.#resolve = null;
    }
  }
  async next() {
    if (!this.#current) {
      if (this.#batches.length === 0) {
        let promise = new Promise((resolve) => {
          this.#resolve = resolve;
        });
        this.#requestNextBatch();
        await promise;
      }
      let next = this.#batches.shift();
      assert(next, "No next batch");
      this.#current = next;
    }
    let result = this.#current.data.next();
    if (result.done) {
      if (this.#current.last) {
        return { done: true, value: void 0 };
      }
      this.#current = null;
      return this.next();
    }
    return {
      done: false,
      value: { row: result.value, index: this.#index++ }
    };
  }
};

// lib/utils/formatting.ts
import { Temporal } from "https://esm.sh/@js-temporal/polyfill@0.4.4";
import * as arrow from "https://esm.sh/apache-arrow@16.1.0";
function fmt(_arrowDataTypeValue, format3, log = false) {
  return (value) => {
    if (log)
      console.log(value);
    if (value === void 0 || value === null) {
      return stringify(value);
    }
    return format3(value);
  };
}
function stringify(x) {
  return `${x}`;
}
function formatDataType(type) {
  if (arrow.DataType.isLargeBinary(type))
    return "large binary";
  if (arrow.DataType.isLargeUtf8(type))
    return "large utf8";
  return type.toString().toLowerCase().replace("<second>", "[s]").replace("<millisecond>", "[ms]").replace("<microsecond>", "[\xB5s]").replace("<nanosecond>", "[ns]").replace("<day>", "[day]").replace("dictionary<", "dict<");
}
function formatterForValue(type) {
  if (arrow.DataType.isNull(type)) {
    return fmt(type.TValue, stringify);
  }
  if (arrow.DataType.isInt(type) || arrow.DataType.isFloat(type)) {
    return fmt(type.TValue, (value) => {
      if (Number.isNaN(value))
        return "NaN";
      return value === 0 ? "0" : value.toLocaleString("en");
    });
  }
  if (arrow.DataType.isBinary(type) || arrow.DataType.isFixedSizeBinary(type) || arrow.DataType.isLargeBinary(type)) {
    return fmt(type.TValue, (bytes) => {
      let maxlen = 32;
      let result = "b'";
      for (let i = 0; i < Math.min(bytes.length, maxlen); i++) {
        const byte = bytes[i];
        if (byte >= 32 && byte <= 126) {
          result += String.fromCharCode(byte);
        } else {
          result += "\\x" + ("00" + byte.toString(16)).slice(-2);
        }
      }
      if (bytes.length > maxlen)
        result += "...";
      result += "'";
      return result;
    });
  }
  if (arrow.DataType.isUtf8(type) || arrow.DataType.isLargeUtf8(type)) {
    return fmt(type.TValue, (text) => text);
  }
  if (arrow.DataType.isBool(type)) {
    return fmt(type.TValue, stringify);
  }
  if (arrow.DataType.isDecimal(type)) {
    return fmt(type.TValue, () => "TODO");
  }
  if (arrow.DataType.isDate(type)) {
    return fmt(type.TValue, (ms) => {
      return Temporal.Instant.fromEpochMilliseconds(ms).toZonedDateTimeISO("UTC").toPlainDate().toString();
    });
  }
  if (arrow.DataType.isTime(type)) {
    return fmt(type.TValue, (ms) => {
      return instantFromTimeUnit(ms, type.unit).toZonedDateTimeISO("UTC").toPlainTime().toString();
    });
  }
  if (arrow.DataType.isTimestamp(type)) {
    return fmt(type.TValue, (ms) => {
      return Temporal.Instant.fromEpochMilliseconds(ms).toZonedDateTimeISO("UTC").toPlainDateTime().toString();
    });
  }
  if (arrow.DataType.isInterval(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isDuration(type)) {
    return fmt(type.TValue, (bigintValue) => {
      return durationFromTimeUnit(bigintValue, type.unit).toString();
    });
  }
  if (arrow.DataType.isList(type)) {
    return fmt(type.TValue, (value) => {
      return value.toString();
    });
  }
  if (arrow.DataType.isStruct(type)) {
    return fmt(type.TValue, (value) => {
      return value.toString();
    });
  }
  if (arrow.DataType.isUnion(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isMap(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isDictionary(type)) {
    let formatter = formatterForValue(type.dictionary);
    return fmt(type.TValue, formatter);
  }
  return () => `Unsupported type: ${type}`;
}
function instantFromTimeUnit(value, unit) {
  if (unit === arrow.TimeUnit.SECOND) {
    if (typeof value === "bigint")
      value = Number(value);
    return Temporal.Instant.fromEpochSeconds(value);
  }
  if (unit === arrow.TimeUnit.MILLISECOND) {
    if (typeof value === "bigint")
      value = Number(value);
    return Temporal.Instant.fromEpochMilliseconds(value);
  }
  if (unit === arrow.TimeUnit.MICROSECOND) {
    if (typeof value === "number")
      value = BigInt(value);
    return Temporal.Instant.fromEpochMicroseconds(value);
  }
  if (unit === arrow.TimeUnit.NANOSECOND) {
    if (typeof value === "number")
      value = BigInt(value);
    return Temporal.Instant.fromEpochNanoseconds(value);
  }
  throw new Error("Invalid TimeUnit");
}
function durationFromTimeUnit(value, unit) {
  value = Number(value);
  if (unit === arrow.TimeUnit.SECOND) {
    return Temporal.Duration.from({ seconds: value });
  }
  if (unit === arrow.TimeUnit.MILLISECOND) {
    return Temporal.Duration.from({ milliseconds: value });
  }
  if (unit === arrow.TimeUnit.MICROSECOND) {
    return Temporal.Duration.from({ microseconds: value });
  }
  if (unit === arrow.TimeUnit.NANOSECOND) {
    return Temporal.Duration.from({ nanoseconds: value });
  }
  throw new Error("Invalid TimeUnit");
}

// lib/clients/Histogram.ts
import {
  MosaicClient
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { count, Query } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as mplot from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-plot@0.10.0/+esm";

// lib/utils/CrossfilterHistogramPlot.ts
import { effect, signal } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/deps/d3.ts
var d3_exports = {};
__reExport(d3_exports, d3_selection_star);
__reExport(d3_exports, d3_scale_star);
__reExport(d3_exports, d3_axis_star);
__reExport(d3_exports, d3_format_star);
__reExport(d3_exports, d3_time_format_star);
import * as d3_selection_star from "https://esm.sh/d3-selection@3.0.0";
import * as d3_scale_star from "https://esm.sh/d3-scale@4.0.2";
import * as d3_axis_star from "https://esm.sh/d3-axis@3.0.0";
import * as d3_format_star from "https://esm.sh/d3-format@3.1.0";
import * as d3_time_format_star from "https://esm.sh/d3-time-format@4.1.0";

// lib/utils/tick-formatter-for-bins.ts
var YEAR = "year";
var MONTH = "month";
var DAY = "day";
var HOUR = "hour";
var MINUTE = "minute";
var SECOND = "second";
var MILLISECOND = "millisecond";
var durationSecond = 1e3;
var durationMinute = durationSecond * 60;
var durationHour = durationMinute * 60;
var durationDay = durationHour * 24;
var durationWeek = durationDay * 7;
var durationMonth = durationDay * 30;
var durationYear = durationDay * 365;
var intervals = [
  [SECOND, 1, durationSecond],
  [SECOND, 5, 5 * durationSecond],
  [SECOND, 15, 15 * durationSecond],
  [SECOND, 30, 30 * durationSecond],
  [MINUTE, 1, durationMinute],
  [MINUTE, 5, 5 * durationMinute],
  [MINUTE, 15, 15 * durationMinute],
  [MINUTE, 30, 30 * durationMinute],
  [HOUR, 1, durationHour],
  [HOUR, 3, 3 * durationHour],
  [HOUR, 6, 6 * durationHour],
  [HOUR, 12, 12 * durationHour],
  [DAY, 1, durationDay],
  [DAY, 7, durationWeek],
  [MONTH, 1, durationMonth],
  [MONTH, 3, 3 * durationMonth],
  [YEAR, 1, durationYear]
];
var formatMap = {
  [MILLISECOND]: d3_exports.timeFormat("%L"),
  [SECOND]: d3_exports.timeFormat("%S s"),
  [MINUTE]: d3_exports.timeFormat("%H:%M"),
  [HOUR]: d3_exports.timeFormat("%H:%M"),
  [DAY]: d3_exports.timeFormat("%b %d"),
  [MONTH]: d3_exports.timeFormat("%b %Y"),
  [YEAR]: d3_exports.timeFormat("%Y")
};
function tickFormatterForBins(type, bins) {
  if (type === "number") {
    return d3_exports.format("~s");
  }
  let interval = timeInterval(
    bins[0].x0,
    bins[bins.length - 1].x1,
    bins.length
  );
  return formatMap[interval.interval];
}
function timeInterval(min, max, steps) {
  const span = max - min;
  const target = span / steps;
  let i = 0;
  while (i < intervals.length && intervals[i][2] < target) {
    i++;
  }
  if (i === intervals.length) {
    return { interval: YEAR, step: binStep(span, steps) };
  }
  if (i > 0) {
    let interval = intervals[target / intervals[i - 1][2] < intervals[i][2] / target ? i - 1 : i];
    return { interval: interval[0], step: interval[1] };
  }
  return { interval: MILLISECOND, step: binStep(span, steps, 1) };
}
function binStep(span, steps, minstep = 0, logb = Math.LN10) {
  let v;
  const level = Math.ceil(Math.log(steps) / logb);
  let step = Math.max(
    minstep,
    Math.pow(10, Math.round(Math.log(span) / logb) - level)
  );
  while (Math.ceil(span / step) > steps)
    step *= 10;
  const div = [5, 2];
  for (let i = 0, n = div.length; i < n; ++i) {
    v = step / div[i];
    if (v >= minstep && span / v <= steps)
      step = v;
  }
  return step;
}

// lib/utils/CrossfilterHistogramPlot.ts
function CrossfilterHistogramPlot(bins, {
  type = "number",
  width = 125,
  height = 40,
  marginTop = 0,
  marginRight = 2,
  marginBottom = 12,
  marginLeft = 2,
  nullCount = 0,
  fillColor = "var(--primary)",
  nullFillColor = "var(--secondary)",
  backgroundBarColor = "var(--moon-gray)"
}) {
  let hovered = signal(void 0);
  let nullBinWidth = nullCount === 0 ? 0 : 5;
  let spacing = nullBinWidth ? 4 : 0;
  let extent = (
    /** @type {const} */
    [
      Math.min(...bins.map((d) => d.x0)),
      Math.max(...bins.map((d) => d.x1))
    ]
  );
  let x = type === "date" ? d3_exports.scaleUtc() : d3_exports.scaleLinear();
  x.domain(extent).range([marginLeft + nullBinWidth + spacing, width - marginRight]).nice();
  let y = d3_exports.scaleLinear().domain([0, Math.max(nullCount, ...bins.map((d) => d.length))]).range([height - marginBottom, marginTop]);
  let svg = d3_exports.create("svg").attr("width", width).attr("height", height).attr("viewBox", [0, 0, width, height]).attr("style", "max-width: 100%; height: auto; overflow: visible;");
  {
    svg.append("g").attr("fill", backgroundBarColor).selectAll("rect").data(bins).join("rect").attr("x", (d) => x(d.x0) + 1.5).attr("width", (d) => x(d.x1) - x(d.x0) - 1.5).attr("y", (d) => y(d.length)).attr("height", (d) => y(0) - y(d.length));
  }
  let foregroundBarGroup = svg.append("g").attr("fill", fillColor);
  const axes = svg.append("g").attr("transform", `translate(0,${height - marginBottom})`).call(
    d3_exports.axisBottom(x).tickValues([...x.domain(), 0]).tickFormat(tickFormatterForBins(type, bins)).tickSize(2.5)
  ).call((g) => {
    g.select(".domain").remove();
    g.attr("class", "gray");
    g.selectAll(".tick text").attr("text-anchor", (_, i) => ["start", "end", "start"][i]).attr("dx", (_, i) => ["-0.25em", "0.25em", "-0.25em"][i]);
  });
  const hoveredTickGroup = axes.node()?.querySelectorAll(".tick")[2];
  assert(hoveredTickGroup, "invariant");
  const hoveredTick = d3_exports.select(hoveredTickGroup);
  const hoverLabelBackground = hoveredTick.insert("rect", ":first-child").attr("width", 20).attr("height", 20).style("fill", "white");
  const fmt2 = type === "number" ? d3_exports.format(".3s") : tickFormatterForBins(type, bins);
  let [xmin, xmax] = x.domain();
  effect(() => {
    hoveredTick.attr("transform", `translate(${x(hovered.value ?? xmin)},0)`).attr("visibility", hovered.value ? "visible" : "hidden");
    hoveredTick.selectAll("text").text(`${fmt2(hovered.value ?? xmin)}`).attr("visibility", hovered.value ? "visible" : "hidden");
    const hoveredTickText = hoveredTick.select("text").node();
    const bbox = hoveredTickText.getBBox();
    const cond = x(hovered.value ?? xmin) + bbox.width > x(xmax);
    hoveredTickText.setAttribute("text-anchor", cond ? "end" : "start");
    hoveredTickText.setAttribute("dx", cond ? "-0.25em" : "0.25em");
    hoverLabelBackground.attr("visibility", hovered.value ? "visible" : "hidden").attr("transform", `translate(${(cond ? -bbox.width : 0) - 2.5}, 2.5)`).attr("width", bbox.width + 5).attr("height", bbox.height + 5);
  });
  let foregroundNullGroup = void 0;
  if (nullCount > 0) {
    let xnull = d3_exports.scaleLinear().range([marginLeft, marginLeft + nullBinWidth]);
    svg.append("g").attr("fill", backgroundBarColor).append("rect").attr("x", xnull(0)).attr("width", xnull(1) - xnull(0)).attr("y", y(nullCount)).attr("height", y(0) - y(nullCount));
    foregroundNullGroup = svg.append("g").attr("fill", nullFillColor).attr("color", nullFillColor);
    foregroundNullGroup.append("rect").attr("x", xnull(0)).attr("width", xnull(1) - xnull(0));
    let axisGroup = foregroundNullGroup.append("g").attr("transform", `translate(0,${height - marginBottom})`).append("g").attr("transform", `translate(${xnull(0.5)}, 0)`).attr("class", "tick");
    axisGroup.append("line").attr("stroke", "currentColor").attr("y2", 2.5);
    axisGroup.append("text").attr("fill", "currentColor").attr("y", 4.5).attr("dy", "0.71em").attr("text-anchor", "middle").text("\u2205").attr("font-size", "0.9em").attr("font-family", "var(--sans-serif)").attr("font-weight", "normal");
  }
  svg.selectAll(".tick").attr("font-family", "var(--sans-serif)").attr("font-weight", "normal");
  function render(bins2, nullCount2) {
    foregroundBarGroup.selectAll("rect").data(bins2).join("rect").attr("x", (d) => x(d.x0) + 1.5).attr("width", (d) => x(d.x1) - x(d.x0) - 1.5).attr("y", (d) => y(d.length)).attr("height", (d) => y(0) - y(d.length));
    foregroundNullGroup?.select("rect").attr("y", y(nullCount2)).attr("height", y(0) - y(nullCount2));
  }
  let scales = {
    x: Object.assign(x, {
      type: "linear",
      domain: x.domain(),
      range: x.range()
    }),
    y: Object.assign(y, {
      type: "linear",
      domain: y.domain(),
      range: y.range()
    })
  };
  let node = svg.node();
  assert(node, "Infallable");
  node.addEventListener("mousemove", (event) => {
    const relativeX = event.clientX - node.getBoundingClientRect().left;
    hovered.value = clamp(x.invert(relativeX), xmin, xmax);
  });
  node.addEventListener("mouseleave", () => {
    hovered.value = void 0;
  });
  render(bins, nullCount);
  return Object.assign(node, {
    /** @param {string} type */
    scale(type2) {
      let scale = scales[type2];
      assert(scale, "Invalid scale type");
      return scale;
    },
    /**
     * @param {Array<Bin>} bins
     * @param {{ nullCount: number }} opts
     */
    update(bins2, { nullCount: nullCount2 }) {
      render(bins2, nullCount2);
    },
    reset() {
      render(bins, nullCount);
    }
  });
}
function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

// lib/clients/Histogram.ts
var Histogram = class extends MosaicClient {
  #source;
  #el = document.createElement("div");
  #select;
  #interval = void 0;
  #initialized = false;
  #fieldInfo;
  svg;
  constructor(options) {
    super(options.filterBy);
    this.#source = options;
    let bin2 = mplot.bin(options.column)(this, "x");
    this.#select = { x1: bin2.x1, x2: bin2.x2, y: count() };
    this.#interval = new mplot.Interval1D(this, {
      channel: "x",
      selection: this.filterBy,
      field: this.#source.column,
      brush: void 0
    });
  }
  fields() {
    return [
      {
        table: this.#source.table,
        column: this.#source.column,
        stats: ["min", "max"]
      }
    ];
  }
  fieldInfo(info) {
    this.#fieldInfo = info[0];
    return this;
  }
  /**
   * Return a query specifying the data needed by this Mark client.
   * @param filter The filtering criteria to apply in the query.
   * @returns The client query
   */
  query(filter = []) {
    return Query.from({ source: this.#source.table }).select(this.#select).groupby(["x1", "x2"]).where(filter);
  }
  /**
   * Provide query result data to the mark.
   */
  queryResult(data) {
    let bins = Array.from(data, (d) => ({
      x0: d.x1,
      x1: d.x2,
      length: d.y
    }));
    let nullCount = 0;
    let nullBinIndex = bins.findIndex((b) => b.x0 == null);
    if (nullBinIndex >= 0) {
      nullCount = bins[nullBinIndex].length;
      bins.splice(nullBinIndex, 1);
    }
    if (!this.#initialized) {
      this.svg = CrossfilterHistogramPlot(bins, {
        nullCount,
        type: this.#source.type
      });
      this.#interval?.init(this.svg, null);
      this.#el.appendChild(this.svg);
      this.#initialized = true;
    } else {
      this.svg?.update(bins, { nullCount });
    }
    return this;
  }
  /* Required by the Mark interface */
  type = "rectY";
  /** Required by `mplot.bin` to get the field info. */
  channelField(channel) {
    assert(channel === "x");
    assert(this.#fieldInfo, "No field info yet");
    return this.#fieldInfo;
  }
  get plot() {
    return {
      node: () => this.#el,
      getAttribute(_name) {
        return void 0;
      }
    };
  }
};

// lib/clients/ValueCounts.ts
import { clausePoint, MosaicClient as MosaicClient2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import {
  column,
  count as count2,
  Query as Query2,
  sql,
  sum
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import { effect as effect3 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/utils/ValueCountsPlot.ts
import { effect as effect2, signal as signal2 } from "https://esm.sh/@preact/signals-core@1.6.1";
function ValueCountsPlot(data, {
  width = 125,
  height = 30,
  marginBottom = 12,
  marginRight = 2,
  marginLeft = 2,
  fillColor = "var(--primary)",
  nullFillColor = "var(--secondary)",
  backgroundBarColor = "rgb(226, 226, 226)"
} = {}) {
  let root = document.createElement("div");
  root.style.position = "relative";
  let container = document.createElement("div");
  Object.assign(container.style, {
    width: `${width}px`,
    height: `${height}px`,
    display: "flex",
    borderRadius: "5px",
    overflow: "hidden"
  });
  let bars = createBars(data, {
    width,
    height,
    marginRight,
    marginLeft,
    fillColor,
    nullFillColor,
    backgroundBarColor
  });
  for (let bar of bars.elements) {
    container.appendChild(bar);
  }
  let text = createTextOutput();
  let hovering = signal2(void 0);
  let selected = signal2(void 0);
  let counts = signal2(data);
  let hitArea = document.createElement("div");
  Object.assign(hitArea.style, {
    position: "absolute",
    top: "0",
    left: "-5px",
    width: `${width + 10}px`,
    height: `${height + marginBottom}px`,
    backgroundColor: "rgba(255, 255, 255, 0.01)",
    cursor: "pointer"
  });
  hitArea.addEventListener("mousemove", (event) => {
    hovering.value = bars.nearestX(event);
  });
  hitArea.addEventListener("mouseout", () => {
    hovering.value = void 0;
  });
  hitArea.addEventListener("mousedown", (event) => {
    let next = bars.nearestX(event);
    selected.value = selected.value === next ? void 0 : next;
  });
  effect2(() => {
    text.textContent = bars.textFor(hovering.value ?? selected.value);
    bars.render(counts.value, hovering.value, selected.value);
  });
  root.appendChild(container);
  root.appendChild(text);
  root.appendChild(hitArea);
  return Object.assign(root, { selected, data: counts });
}
function createBar(opts) {
  let { title, fillColor, textColor, width, height } = opts;
  let bar = document.createElement("div");
  bar.title = title;
  Object.assign(bar.style, {
    background: createSplitBarFill({
      color: fillColor,
      bgColor: "var(--moon-gray)",
      frac: 50
    }),
    width: `${width}px`,
    height: `${height}px`,
    borderColor: "white",
    borderWidth: "0px 1px 0px 0px",
    borderStyle: "solid",
    opacity: 1,
    textAlign: "center",
    position: "relative",
    display: "flex",
    overflow: "hidden",
    alignItems: "center",
    fontWeight: 400,
    fontFamily: "var(--sans-serif)",
    boxSizing: "border-box"
  });
  let span = document.createElement("span");
  Object.assign(span.style, {
    overflow: "hidden",
    width: `calc(100% - 4px)`,
    left: "0px",
    position: "absolute",
    padding: "0px 2px",
    color: textColor
  });
  if (width > 10) {
    span.textContent = title;
  }
  bar.appendChild(span);
  return bar;
}
function prepareData(data) {
  let arr = data.toArray().toSorted((a, b) => b.total - a.total);
  let total = arr.reduce((acc, d) => acc + d.total, 0);
  return {
    bins: arr.filter(
      (d) => d.key !== "__quak_null__" && d.key !== "__quak_unique__"
    ),
    nullCount: arr.find((d) => d.key === "__quak_null__")?.total ?? 0,
    uniqueCount: arr.find((d) => d.key === "__quak_unique__")?.total ?? 0,
    total
  };
}
function createBars(data, opts) {
  let source = prepareData(data);
  let x = d3_exports.scaleLinear().domain([0, source.total]).range([opts.marginLeft, opts.width - opts.marginRight]);
  let thresh = 20;
  let bars = [];
  for (let d of source.bins.slice(0, thresh)) {
    let bar = createBar({
      title: d.key,
      fillColor: opts.fillColor,
      textColor: "white",
      width: x(d.total),
      height: opts.height
    });
    bars.push(Object.assign(bar, { data: d }));
  }
  let hoverBar = createVirtualSelectionBar(opts);
  let selectBar = createVirtualSelectionBar(opts);
  let virtualBar;
  if (source.bins.length > thresh) {
    let total = source.bins.slice(thresh).reduce(
      (acc, d) => acc + d.total,
      0
    );
    virtualBar = Object.assign(document.createElement("div"), {
      title: "__quak_virtual__"
    });
    Object.assign(virtualBar.style, {
      width: `${x(total)}px`,
      height: "100%",
      borderColor: "white",
      borderWidth: "0px 1px 0px 0px",
      borderStyle: "solid",
      opacity: 1
    });
    let vbars = document.createElement("div");
    Object.assign(vbars.style, {
      width: "100%",
      height: "100%",
      background: `repeating-linear-gradient(to right, ${opts.fillColor} 0px, ${opts.fillColor} 1px, white 1px, white 2px)`
    });
    virtualBar.appendChild(vbars);
    virtualBar.appendChild(hoverBar);
    virtualBar.appendChild(selectBar);
    Object.defineProperty(virtualBar, "data", {
      value: source.bins.slice(thresh)
    });
    bars.push(virtualBar);
  }
  if (source.uniqueCount) {
    let bar = createBar({
      title: "unique",
      fillColor: opts.backgroundBarColor,
      textColor: "var(--mid-gray)",
      width: x(source.uniqueCount),
      height: opts.height
    });
    bar.title = "__quak_unique__";
    bars.push(Object.assign(bar, {
      data: {
        key: "__quak_unique__",
        total: source.uniqueCount
      }
    }));
  }
  if (source.nullCount) {
    let bar = createBar({
      title: "null",
      fillColor: opts.nullFillColor,
      textColor: "white",
      width: x(source.nullCount),
      height: opts.height
    });
    bar.title = "__quak_null__";
    bars.push(Object.assign(bar, {
      data: {
        key: "__quak_null__",
        total: source.uniqueCount
      }
    }));
  }
  let first = bars[0];
  let last = bars[bars.length - 1];
  if (first === last) {
    first.style.borderRadius = "5px";
  } else {
    first.style.borderRadius = "5px 0px 0px 5px";
    last.style.borderRadius = "0px 5px 5px 0px";
  }
  function virtualBin(key) {
    assert(virtualBar);
    let voffset = bars.slice(0, thresh).map((b) => b.getBoundingClientRect().width).reduce((a, b) => a + b, 0);
    let vbins = virtualBar.data;
    let rect = virtualBar.getBoundingClientRect();
    let dx = rect.width / vbins.length;
    let idx = vbins.findIndex((d) => d.key === key);
    assert(idx !== -1, `key ${key} not found in virtual bins`);
    return {
      ...vbins[idx],
      x: dx * idx + voffset
    };
  }
  function reset(opactiy) {
    bars.forEach((bar) => {
      if (bar.title === "__quak_virtual__") {
        let vbars = bar.firstChild;
        vbars.style.opacity = opactiy.toString();
        vbars.style.background = createVirtualBarRepeatingBackground({
          color: opts.fillColor
        });
      } else {
        bar.style.opacity = opactiy.toString();
        bar.style.background = createSplitBarFill({
          color: bar.title === "__quak_unique__" ? opts.backgroundBarColor : bar.title === "__quak_null__" ? opts.nullFillColor : opts.fillColor,
          bgColor: opts.backgroundBarColor,
          frac: 1
        });
      }
      bar.style.borderColor = "white";
      bar.style.borderWidth = "0px 1px 0px 0px";
      bar.style.removeProperty("box-shadow");
    });
    bars[bars.length - 1].style.borderWidth = "0px";
    hoverBar.style.visibility = "hidden";
    selectBar.style.visibility = "hidden";
  }
  function hover(key, selected) {
    let bar = bars.find((b) => b.data.key === key);
    if (bar !== void 0) {
      bar.style.opacity = "1";
      return;
    }
    let vbin = virtualBin(key);
    hoverBar.title = vbin.key;
    hoverBar.data = vbin;
    hoverBar.style.opacity = selected ? "0.25" : "1";
    hoverBar.style.left = `${vbin.x}px`;
    hoverBar.style.visibility = "visible";
  }
  function select2(key) {
    let bar = bars.find((b) => b.data.key === key);
    if (bar !== void 0) {
      bar.style.opacity = "1";
      bar.style.boxShadow = "inset 0 0 0 1.2px black";
      return;
    }
    let vbin = virtualBin(key);
    selectBar.style.opacity = "1";
    selectBar.title = vbin.key;
    selectBar.data = vbin;
    selectBar.style.left = `${vbin.x}px`;
    selectBar.style.visibility = "visible";
  }
  let counts = Object.fromEntries(
    Array.from(data.toArray(), (d) => [d.key, d.total])
  );
  return {
    elements: bars,
    nearestX(event) {
      let bar = nearestX(event, bars);
      if (!bar)
        return;
      if (bar.title !== "__quak_virtual__") {
        return bar.data.key;
      }
      let rect = bar.getBoundingClientRect();
      let mouseX = event.clientX - rect.left;
      let data2 = bar.data;
      let idx = Math.floor(mouseX / rect.width * data2.length);
      return data2[idx].key;
    },
    render(data2, hovering, selected) {
      reset(hovering || selected ? 0.4 : 1);
      let update = Object.fromEntries(
        Array.from(data2.toArray(), (d) => [d.key, d.total])
      );
      let total = Object.values(update).reduce((a, b) => a + b, 0);
      for (let bar of bars) {
        if (bar.title === "__quak_virtual__") {
          let vbars = bar.firstChild;
          vbars.style.background = createVirtualBarRepeatingBackground({
            color: total < source.total || selected ? opts.backgroundBarColor : opts.fillColor
          });
        } else {
          let key = bar.data.key;
          let frac = (update[key] ?? 0) / counts[key];
          if (selected)
            frac = key === selected ? frac : 0;
          bar.style.background = createSplitBarFill({
            color: bar.title === "__quak_unique__" ? opts.backgroundBarColor : bar.title === "__quak_null__" ? opts.nullFillColor : opts.fillColor,
            bgColor: opts.backgroundBarColor,
            frac: isNaN(frac) ? 0 : frac
          });
        }
      }
      if (hovering !== void 0) {
        hover(hovering, selected);
      }
      if (selected !== void 0) {
        select2(selected);
      }
    },
    textFor(key) {
      if (key === void 0) {
        let ncats = data.numRows;
        return `${ncats.toLocaleString()} categor${ncats === 1 ? "y" : "ies"}`;
      }
      if (key === "__quak_unique__") {
        return `${source.uniqueCount.toLocaleString()} unique value${source.uniqueCount === 1 ? "" : "s"}`;
      }
      if (key === "__quak_null__") {
        return "null";
      }
      return key.toString();
    }
  };
}
function createTextOutput() {
  let node = document.createElement("div");
  Object.assign(node.style, {
    pointerEvents: "none",
    height: "15px",
    maxWidth: "100%",
    overflow: "hidden",
    textOverflow: "ellipsis",
    position: "absolute",
    fontWeight: 400,
    marginTop: "1.5px",
    color: "var(--mid-gray)"
  });
  return node;
}
function createVirtualSelectionBar(opts) {
  let node = document.createElement("div");
  Object.assign(node.style, {
    position: "absolute",
    top: "0",
    width: "1.5px",
    height: "100%",
    backgroundColor: opts.fillColor,
    pointerEvents: "none",
    visibility: "hidden"
  });
  return Object.assign(node, {
    data: { key: "", total: 0 }
  });
}
function nearestX({ clientX }, bars) {
  for (let bar of bars) {
    let rect = bar.getBoundingClientRect();
    if (clientX >= rect.left && clientX <= rect.right) {
      return bar;
    }
  }
}
function createSplitBarFill(options) {
  let { color, bgColor, frac } = options;
  let p = frac * 100;
  return `linear-gradient(to top, ${color} ${p}%, ${bgColor} ${p}%, ${bgColor} ${100 - p}%)`;
}
function createVirtualBarRepeatingBackground({ color }) {
  return `repeating-linear-gradient(to right, ${color} 0px, ${color} 1px, white 1px, white 2px)`;
}

// lib/clients/ValueCounts.ts
var ValueCounts = class extends MosaicClient2 {
  #table;
  #column;
  #el = document.createElement("div");
  #plot;
  constructor(options) {
    super(options.filterBy);
    this.#table = options.table;
    this.#column = options.column;
    options.filterBy.addEventListener("value", async () => {
      let filters = options.filterBy.predicate();
      let query = this.query(filters);
      if (this.#plot) {
        let data = await this.coordinator.query(query);
        this.#plot.data.value = data;
      }
    });
  }
  query(filter = []) {
    let counts = Query2.from({ source: this.#table }).select({
      value: sql`CASE
					WHEN ${column(this.#column)} IS NULL THEN '__quak_null__'
					ELSE ${column(this.#column)}
				END`,
      count: count2()
    }).groupby("value").where(filter);
    return Query2.with({ counts }).select(
      {
        key: sql`CASE
						WHEN "count" = 1 AND "value" != '__quak_null__' THEN '__quak_unique__'
						ELSE "value"
					END`,
        total: sum("count")
      }
    ).from("counts").groupby("key");
  }
  queryResult(data) {
    if (!this.#plot) {
      let plot = this.#plot = ValueCountsPlot(data);
      this.#el.appendChild(plot);
      effect3(() => {
        let clause = this.clause(plot.selected.value);
        this.filterBy.update(clause);
      });
    } else {
      this.#plot.data.value = data;
    }
    return this;
  }
  clause(value) {
    let update = value === "__quak_null__" ? null : value;
    return clausePoint(this.#column, update, {
      source: this
    });
  }
  reset() {
    assert(this.#plot, "ValueCounts plot not initialized");
    this.#plot.selected.value = void 0;
  }
  get plot() {
    return {
      node: () => this.#el
    };
  }
};

// lib/clients/DataTable.ts
import { signal as signal4 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/clients/styles.css?raw
var styles_default = ':host {\n	all: initial;\n	--sans-serif: -apple-system, BlinkMacSystemFont, "avenir next", avenir, helvetica, "helvetica neue", ubuntu, roboto, noto, "segoe ui", arial, sans-serif;\n	--light-silver: #efefef;\n	--spacing-none: 0;\n	--white: #fff;\n	--gray: #929292;\n	--dark-gray: #333;\n	--moon-gray: #c4c4c4;\n	--mid-gray: #6e6e6e;\n\n	--stone-blue: #64748b;\n	--yellow-gold: #ca8a04;\n\n	--teal: #027982;\n	--dark-pink: #D35A5F;\n\n	--light-blue: #7E93CF;\n	--dark-yellow-gold: #A98447;\n\n	--purple: #987fd3;\n\n	--primary: var(--stone-blue);\n	--secondary: var(--yellow-gold);\n}\n\n.highlight {\n	background-color: var(--light-silver);\n}\n\n.highlight-cell {\n	border: 1px solid var(--moon-gray);\n}\n\n.quak {\n  border-radius: 0.2rem;\n  border: 1px solid var(--light-silver);\n  overflow-y: auto;\n}\n\ntable {\n  border-collapse: separate;\n  border-spacing: 0;\n  white-space: nowrap;\n  box-sizing: border-box;\n\n  margin: var(--spacing-none);\n  color: var(--dark-gray);\n  font: 13px / 1.2 var(--sans-serif);\n\n  width: 100%;\n}\n\nthead {\n  position: sticky;\n  vertical-align: top;\n  text-align: left;\n  top: 0;\n}\n\ntd {\n  border: 1px solid var(--light-silver);\n  border-bottom: solid 1px transparent;\n  border-right: solid 1px transparent;\n  overflow: hidden;\n  -o-text-overflow: ellipsis;\n  text-overflow: ellipsis;\n  padding: 4px 6px;\n}\n\ntr:first-child td {\n  border-top: solid 1px transparent;\n}\n\nth {\n  display: table-cell;\n  vertical-align: inherit;\n  font-weight: bold;\n  text-align: -internal-center;\n  unicode-bidi: isolate;\n\n  position: relative;\n  background: var(--white);\n  border-bottom: solid 1px var(--light-silver);\n  border-left: solid 1px var(--light-silver);\n  padding: 5px 6px;\n  user-select: none;\n}\n\n.number, .date {\n  font-variant-numeric: tabular-nums;\n}\n\n.gray {\n  color: var(--gray);\n}\n\n.number {\n  text-align: right;\n}\n\ntd:nth-child(1), th:nth-child(1) {\n  font-variant-numeric: tabular-nums;\n  text-align: center;\n  color: var(--moon-gray);\n  padding: 0 4px;\n}\n\ntd:first-child, th:first-child {\n  border-left: none;\n}\n\nth:first-child {\n  border-left: none;\n  vertical-align: top;\n  width: 20px;\n  padding: 7px;\n}\n\ntd:nth-last-child(2), th:nth-last-child(2) {\n  border-right: 1px solid var(--light-silver);\n}\n\ntr:first-child td {\n	border-top: solid 1px transparent;\n}\n\n.resize-handle {\n	width: 5px;\n	height: 100%;\n	background-color: transparent;\n	position: absolute;\n	right: -2.5px;\n	top: 0;\n	cursor: ew-resize;\n	z-index: 1;\n}\n\n.quak .sort-button {\n	cursor: pointer;\n	background-color: var(--white);\n	user-select: none;\n}\n\n.status-bar {\n	display: flex;\n	justify-content: flex-end;\n	font-family: var(--sans-serif);\n	margin-right: 10px;\n	margin-top: 5px;\n}\n\n.status-bar button {\n	border: none;\n	background-color: var(--white);\n	color: var(--primary);\n	font-weight: 600;\n	font-size: 0.875rem;\n	cursor: pointer;\n	margin-right: 5px;\n}\n\n.status-bar span {\n	color: var(--gray);\n	font-weight: 400;\n	font-size: 0.75rem;\n	font-variant-numeric: tabular-nums;\n}\n';

// lib/clients/StatusBar.ts
import { MosaicClient as MosaicClient3 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { count as count3, Query as Query3 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
var StatusBar = class extends MosaicClient3 {
  #table;
  #el = document.createElement("div");
  #button;
  #span;
  #totalRows = void 0;
  constructor(options) {
    super(options.filterBy);
    this.#table = options.table;
    this.#button = document.createElement("button");
    this.#button.innerText = "Reset";
    this.#span = document.createElement("span");
    let div = document.createElement("div");
    div.appendChild(this.#button);
    div.appendChild(this.#span);
    this.#el.appendChild(div);
    this.#el.classList.add("status-bar");
    this.#button.addEventListener("mousedown", () => {
      if (!this.filterBy)
        return;
      for (let { source } of this.filterBy.clauses) {
        if (!isInteractor(source)) {
          console.warn("Skipping non-interactor source", source);
          continue;
        }
        source.reset();
        this.filterBy.update(source.clause());
      }
    });
    this.#button.style.visibility = "hidden";
    this.filterBy?.addEventListener("value", () => {
      if (this.filterBy?.clauses.length === 0) {
        this.#button.style.visibility = "hidden";
      } else {
        this.#button.style.visibility = "visible";
      }
    });
  }
  query(filter = []) {
    let query = Query3.from(this.#table).select({ count: count3() }).where(filter);
    return query;
  }
  queryResult(table) {
    let count4 = Number(table.get(0)?.count ?? 0);
    if (!this.#totalRows) {
      this.#totalRows = count4;
    }
    let countStr = count4.toLocaleString();
    if (count4 == this.#totalRows) {
      this.#span.innerText = `${countStr} rows`;
    } else {
      let totalStr = this.#totalRows.toLocaleString();
      this.#span.innerText = `${countStr} of ${totalStr} rows`;
    }
    return this;
  }
  node() {
    return this.#el;
  }
};
function isObject(x) {
  return typeof x === "object" && x !== null && !Array.isArray(x);
}
function isInteractor(x) {
  return isObject(x) && "clause" in x && "reset" in x;
}

// lib/clients/DataTable.ts
var DataTable = class extends MosaicClient4 {
  /** source of the data */
  #meta;
  /** for the component */
  #root = document.createElement("div");
  /** shadow root for the component */
  #shadowRoot = this.#root.attachShadow({ mode: "open" });
  /** header of the table */
  #thead = document.createElement("thead");
  /** body of the table */
  #tbody = document.createElement("tbody");
  /** The SQL order by */
  #orderby = [];
  /** template row for data */
  #templateRow = void 0;
  /** div containing the table */
  #tableRoot;
  /** offset into the data */
  #offset = 0;
  /** number of rows to fetch */
  #limit = 100;
  /** whether an internal request is pending */
  #pendingInternalRequest = true;
  /** number of rows to display */
  #rows = 11.5;
  /** height of a row */
  #rowHeight = 22;
  /** width of a column */
  #columnWidth = 125;
  /** height of the header */
  #headerHeight = "94px";
  /** the formatter for the data table entries */
  #format;
  /** @type {AsyncBatchReader<arrow.StructRowProxy> | null} */
  #reader = null;
  #sql = signal4(void 0);
  constructor(source) {
    super(Selection2.crossfilter());
    this.#format = formatof(source.schema);
    this.#meta = source;
    let maxHeight = `${(this.#rows + 1) * this.#rowHeight - 1}px`;
    if (source.height) {
      this.#rows = Math.floor(source.height / this.#rowHeight);
      maxHeight = `${source.height}px`;
    }
    let root = html`<div class="quak" style=${{
      maxHeight
    }}>`;
    root.appendChild(
      html.fragment`<table style=${{ tableLayout: "fixed" }}>${this.#thead}${this.#tbody}</table>`
    );
    this.#shadowRoot.appendChild(html`<style>${styles_default}</style>`);
    this.#shadowRoot.appendChild(root);
    this.#tableRoot = root;
    addDirectionalScrollWithPreventDefault(this.#tableRoot);
    this.#tableRoot.addEventListener("scroll", async () => {
      let isAtBottom = this.#tableRoot.scrollHeight - this.#tableRoot.scrollTop < this.#rows * this.#rowHeight * 1.5;
      if (isAtBottom) {
        await this.#appendRows(this.#rows);
      }
    });
  }
  get sql() {
    return this.#sql.value;
  }
  fields() {
    return this.#columns.map((column2) => ({
      table: this.#meta.table,
      column: column2,
      stats: []
    }));
  }
  node() {
    return this.#root;
  }
  resize(height) {
    this.#rows = Math.floor(height / this.#rowHeight);
    this.#tableRoot.style.maxHeight = `${height}px`;
    this.#tableRoot.scrollTop = 0;
  }
  get #columns() {
    return this.#meta.schema.fields.map((field) => field.name);
  }
  /**
   * @param {Array<unknown>} filter
   */
  query(filter = []) {
    let query = Query4.from(this.#meta.table).select(this.#columns).where(filter).orderby(
      this.#orderby.filter((o) => o.order !== "unset").map((o) => o.order === "asc" ? asc(o.field) : desc(o.field))
    );
    this.#sql.value = query.clone().toString();
    return query.limit(this.#limit).offset(this.#offset);
  }
  /**
   * A mosiac lifecycle function that is called with the results from `query`.
   * Must be synchronous, and return `this`.
   */
  queryResult(table) {
    if (!this.#pendingInternalRequest) {
      this.#reader = new AsyncBatchReader(() => {
        this.#pendingInternalRequest = true;
        this.requestData(this.#offset + this.#limit);
      });
      this.#tbody.replaceChildren();
      this.#tableRoot.scrollTop = 0;
      this.#offset = 0;
    }
    let batch = table[Symbol.iterator]();
    this.#reader?.enqueueBatch(batch, {
      last: table.numRows < this.#limit
    });
    return this;
  }
  update() {
    if (!this.#pendingInternalRequest) {
      this.#appendRows(this.#rows * 2);
    }
    this.#pendingInternalRequest = false;
    return this;
  }
  requestData(offset = 0) {
    this.#offset = offset;
    let query = this.query(this.filterBy?.predicate(this));
    this.requestQuery(query);
    this.coordinator.prefetch(query.clone().offset(offset + this.#limit));
  }
  fieldInfo(infos) {
    let classes = classof(this.#meta.schema);
    {
      let statusBar = new StatusBar({
        table: this.#meta.table,
        filterBy: this.filterBy
      });
      this.coordinator.connect(statusBar);
      this.#shadowRoot.appendChild(statusBar.node());
    }
    this.#templateRow = html`<tr><td></td>${infos.map((info) => html.fragment`<td class=${classes[info.column]}></td>`)}
			<td style=${{ width: "99%", borderLeft: "none", borderRight: "none" }}></td>
		</tr>`;
    let observer = new IntersectionObserver((entries) => {
      for (let entry of entries) {
        if (!isTableColumnHeaderWithSvg(entry.target))
          continue;
        let vis = entry.target.vis;
        if (!vis)
          continue;
        if (entry.isIntersecting) {
          this.coordinator.connect(vis);
        } else {
          this.coordinator?.disconnect(vis);
        }
      }
    }, {
      root: this.#tableRoot
    });
    let cols = this.#meta.schema.fields.map((field) => {
      let info = infos.find((c) => c.column === field.name);
      assert(info, `No info for column ${field.name}`);
      let vis = void 0;
      if (info.type === "number" || info.type === "date") {
        vis = new Histogram({
          table: this.#meta.table,
          column: field.name,
          type: info.type,
          filterBy: this.filterBy
        });
      } else {
        vis = new ValueCounts({
          table: this.#meta.table,
          column: field.name,
          filterBy: this.filterBy
        });
      }
      let th = thcol(field, this.#columnWidth, vis);
      observer.observe(th);
      return th;
    });
    signals.effect(() => {
      this.#orderby = cols.map((col, i) => ({
        field: this.#columns[i],
        order: col.sortState.value
      }));
      this.requestData();
    });
    this.#thead.appendChild(
      html`<tr style=${{ height: this.#headerHeight }}>
				<th></th>
				${cols}
				<th style=${{ width: "99%", borderLeft: "none", borderRight: "none" }}></th>
			</tr>`
    );
    {
      this.#tableRoot.addEventListener("mouseover", (event) => {
        if (isTableCellElement(event.target) && isTableRowElement(event.target.parentNode)) {
          const cell = event.target;
          const row = event.target.parentNode;
          highlight(cell, row);
        }
      });
      this.#tableRoot.addEventListener("mouseout", (event) => {
        if (isTableCellElement(event.target) && isTableRowElement(event.target.parentNode)) {
          const cell = event.target;
          const row = event.target.parentNode;
          removeHighlight(cell, row);
        }
      });
    }
    return this;
  }
  /** Number of rows to append */
  async #appendRows(nrows) {
    nrows = Math.trunc(nrows);
    while (nrows >= 0) {
      let result = await this.#reader?.next();
      if (!result || result?.done) {
        break;
      }
      this.#appendRow(result.value.row, result.value.index);
      nrows--;
      continue;
    }
  }
  #appendRow(d, i) {
    let itr = this.#templateRow?.cloneNode(true);
    assert(itr, "Must have a data row");
    let td = itr.childNodes[0];
    td.appendChild(document.createTextNode(String(i)));
    for (let j = 0; j < this.#columns.length; ++j) {
      td = itr.childNodes[j + 1];
      td.classList.remove("gray");
      let col = this.#columns[j];
      let stringified = this.#format[col](d[col]);
      if (shouldGrayoutValue(stringified)) {
        td.classList.add("gray");
      }
      let value = document.createTextNode(stringified);
      td.appendChild(value);
    }
    this.#tbody.append(itr);
  }
};
var TRUNCATE = (
  /** @type {const} */
  {
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis"
  }
);
function thcol(field, minWidth, vis) {
  let buttonVisible = signals.signal(false);
  let width = signals.signal(minWidth);
  let sortState = signals.signal(
    "unset"
  );
  function nextSortState() {
    sortState.value = {
      "unset": "asc",
      "asc": "desc",
      "desc": "unset"
    }[sortState.value];
  }
  let svg = html`<svg style=${{ width: "1.5em" }} fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
		<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9L12 5.25L15.75 9" />
		<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75L15.75 15" />
	</svg>`;
  let uparrow = svg.children[0];
  let downarrow = svg.children[1];
  let verticalResizeHandle = html`<div class="resize-handle"></div>`;
  let sortButton = html`<span aria-role="button" class="sort-button" onmousedown=${nextSortState}>${svg}</span>`;
  let th = html`<th style=${{ overflow: "hidden" }}>
		<div style=${{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
			<span style=${{ marginBottom: "5px", maxWidth: "250px", ...TRUNCATE }}>${field.name}</span>
			${sortButton}
		</div>
		${verticalResizeHandle}
		<span class="gray" style=${{ fontWeight: 400, fontSize: "12px", userSelect: "none" }}>${formatDataType(field.type)}</span>
		${vis?.plot?.node()}
	</th>`;
  signals.effect(() => {
    uparrow.setAttribute("stroke", "var(--moon-gray)");
    downarrow.setAttribute("stroke", "var(--moon-gray)");
    let element = { "asc": uparrow, "desc": downarrow, "unset": null }[sortState.value];
    element?.setAttribute("stroke", "var(--dark-gray)");
  });
  signals.effect(() => {
    sortButton.style.visibility = buttonVisible.value ? "visible" : "hidden";
  });
  signals.effect(() => {
    th.style.width = `${width.value}px`;
  });
  th.addEventListener("mouseover", () => {
    if (sortState.value === "unset")
      buttonVisible.value = true;
  });
  th.addEventListener("mouseleave", () => {
    if (sortState.value === "unset")
      buttonVisible.value = false;
  });
  th.addEventListener("dblclick", (event) => {
    if (event.offsetX < sortButton.offsetWidth && event.offsetY < sortButton.offsetHeight) {
      return;
    }
    width.value = minWidth;
  });
  verticalResizeHandle.addEventListener("mousedown", (event) => {
    event.preventDefault();
    let startX = event.clientX;
    let startWidth = th.offsetWidth - parseFloat(getComputedStyle(th).paddingLeft) - parseFloat(getComputedStyle(th).paddingRight);
    function onMouseMove(event2) {
      let dx = event2.clientX - startX;
      width.value = Math.max(minWidth, startWidth + dx);
      verticalResizeHandle.style.backgroundColor = "var(--light-silver)";
    }
    function onMouseUp() {
      verticalResizeHandle.style.backgroundColor = "transparent";
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    }
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  });
  verticalResizeHandle.addEventListener("mouseover", () => {
    verticalResizeHandle.style.backgroundColor = "var(--light-silver)";
  });
  verticalResizeHandle.addEventListener("mouseleave", () => {
    verticalResizeHandle.style.backgroundColor = "transparent";
  });
  return Object.assign(th, { vis, sortState });
}
function formatof(schema) {
  const format3 = /* @__PURE__ */ Object.create(
    null
  );
  for (const field of schema.fields) {
    format3[field.name] = formatterForValue(field.type);
  }
  return format3;
}
function classof(schema) {
  const classes = /* @__PURE__ */ Object.create(null);
  for (const field of schema.fields) {
    if (arrow2.DataType.isInt(field.type) || arrow2.DataType.isFloat(field.type)) {
      classes[field.name] = "number";
    }
    if (arrow2.DataType.isDate(field.type) || arrow2.DataType.isTimestamp(field.type)) {
      classes[field.name] = "date";
    }
  }
  return classes;
}
function highlight(cell, row) {
  if (row.firstChild !== cell && cell !== row.lastElementChild) {
    cell.style.border = "1px solid var(--moon-gray)";
  }
  row.style.backgroundColor = "var(--light-silver)";
}
function removeHighlight(cell, row) {
  cell.style.removeProperty("border");
  row.style.removeProperty("background-color");
}
function isTableCellElement(node) {
  return node?.tagName === "TD";
}
function isTableRowElement(node) {
  return node instanceof HTMLTableRowElement;
}
function shouldGrayoutValue(value) {
  return value === "null" || value === "undefined" || value === "NaN" || value === "TODO";
}
function isTableColumnHeaderWithSvg(node) {
  return node instanceof HTMLTableCellElement && "vis" in node;
}
function asc(field) {
  let expr = desc(field);
  expr._expr[0] = expr._expr[0].replace("DESC", "ASC");
  return expr;
}
function addDirectionalScrollWithPreventDefault(root, scrollThreshold = 10) {
  let accumulatedDeltaX = 0;
  let accumulatedDeltaY = 0;
  root.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      accumulatedDeltaX += event.deltaX;
      accumulatedDeltaY += event.deltaY;
      if (Math.abs(accumulatedDeltaX) > Math.abs(accumulatedDeltaY)) {
        if (Math.abs(accumulatedDeltaX) > scrollThreshold) {
          root.scrollLeft += accumulatedDeltaX;
          accumulatedDeltaX = 0;
          accumulatedDeltaY = 0;
        }
      } else {
        if (Math.abs(accumulatedDeltaY) > scrollThreshold) {
          root.scrollTop += accumulatedDeltaY;
          accumulatedDeltaX = 0;
          accumulatedDeltaY = 0;
        }
      }
    },
    { passive: false }
  );
}

// lib/utils/defer.ts
function defer() {
  let resolve;
  let reject;
  let promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

// lib/widget.ts
var widget_default = () => {
  let coordinator = new mc.Coordinator();
  let schema;
  return {
    async initialize({ model }) {
      let logger = coordinator.logger(_voidLogger());
      let openQueries = /* @__PURE__ */ new Map();
      function send(query, resolve, reject) {
        let id = uuid.v4();
        openQueries.set(id, {
          query,
          startTime: performance.now(),
          resolve,
          reject
        });
        model.send({ ...query, uuid: id });
      }
      model.on("msg:custom", (msg, buffers) => {
        logger.group(`query ${msg.uuid}`);
        logger.log("received message", msg, buffers);
        let query = openQueries.get(msg.uuid);
        openQueries.delete(msg.uuid);
        assert(query, `No query found for ${msg.uuid}`);
        logger.log(
          query.query.toString(),
          (performance.now() - query.startTime).toFixed(1)
        );
        if (msg.error) {
          query.reject(msg.error);
          logger.error(msg.error);
          return;
        } else {
          switch (msg.type) {
            case "arrow": {
              let table = arrow3.tableFromIPC(buffers[0].buffer);
              logger.log("table", table);
              query.resolve(table);
              break;
            }
            case "json": {
              logger.log("json", msg.result);
              query.resolve(msg.result);
              break;
            }
            default: {
              query.resolve({});
              break;
            }
          }
        }
        logger.groupEnd("query");
      });
      coordinator.databaseConnector({
        query(query) {
          let { promise, resolve, reject } = defer();
          send(query, resolve, reject);
          return promise;
        }
      });
      let empty = await coordinator.query(
        Query5.from(model.get("_table_name")).select(...model.get("_columns")).limit(0).toString()
      );
      schema = empty.schema;
      return () => {
        coordinator.clear();
      };
    },
    render({ model, el }) {
      let table = new DataTable({
        table: model.get("_table_name"),
        schema
      });
      coordinator.connect(table);
      effect5(() => {
        model.set("sql", table.sql ?? "");
        model.save_changes();
      });
      el.appendChild(table.node());
    }
  };
};
function _voidLogger() {
  return Object.fromEntries(
    Object.keys(console).map((key) => [key, () => {
    }])
  );
}
export {
  widget_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vbGliL3dpZGdldC50cyIsICIuLi8uLi9saWIvY2xpZW50cy9EYXRhVGFibGUudHMiLCAiLi4vLi4vbGliL3V0aWxzL2Fzc2VydC50cyIsICIuLi8uLi9saWIvdXRpbHMvQXN5bmNCYXRjaFJlYWRlci50cyIsICIuLi8uLi9saWIvdXRpbHMvZm9ybWF0dGluZy50cyIsICIuLi8uLi9saWIvY2xpZW50cy9IaXN0b2dyYW0udHMiLCAiLi4vLi4vbGliL3V0aWxzL0Nyb3NzZmlsdGVySGlzdG9ncmFtUGxvdC50cyIsICIuLi8uLi9saWIvZGVwcy9kMy50cyIsICIuLi8uLi9saWIvdXRpbHMvdGljay1mb3JtYXR0ZXItZm9yLWJpbnMudHMiLCAiLi4vLi4vbGliL2NsaWVudHMvVmFsdWVDb3VudHMudHMiLCAiLi4vLi4vbGliL3V0aWxzL1ZhbHVlQ291bnRzUGxvdC50cyIsICIuLi8uLi9saWIvY2xpZW50cy9zdHlsZXMuY3NzIiwgIi4uLy4uL2xpYi9jbGllbnRzL1N0YXR1c0Jhci50cyIsICIuLi8uLi9saWIvdXRpbHMvZGVmZXIudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbIi8vIEBkZW5vLXR5cGVzPVwiLi9kZXBzL21vc2FpYy1jb3JlLmQudHNcIjtcbmltcG9ydCAqIGFzIG1jIGZyb20gXCJAdXdkYXRhL21vc2FpYy1jb3JlXCI7XG4vLyBAZGVuby10eXBlcz1cIi4vZGVwcy9tb3NhaWMtc3FsLmQudHNcIjtcbmltcG9ydCB7IFF1ZXJ5IH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuaW1wb3J0ICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuaW1wb3J0ICogYXMgdXVpZCBmcm9tIFwiQGx1a2VlZC91dWlkXCI7XG5pbXBvcnQgdHlwZSAqIGFzIGF3IGZyb20gXCJAYW55d2lkZ2V0L3R5cGVzXCI7XG5pbXBvcnQgeyBlZmZlY3QgfSBmcm9tIFwiQHByZWFjdC9zaWduYWxzLWNvcmVcIjtcblxuaW1wb3J0IHsgRGF0YVRhYmxlIH0gZnJvbSBcIi4vY2xpZW50cy9EYXRhVGFibGUudHNcIjtcbmltcG9ydCB7IGFzc2VydCB9IGZyb20gXCIuL3V0aWxzL2Fzc2VydC50c1wiO1xuaW1wb3J0IHsgZGVmZXIgfSBmcm9tIFwiLi91dGlscy9kZWZlci50c1wiO1xuXG50eXBlIE1vZGVsID0ge1xuXHRfdGFibGVfbmFtZTogc3RyaW5nO1xuXHRfY29sdW1uczogQXJyYXk8c3RyaW5nPjtcblx0dGVtcF9pbmRleGVzOiBib29sZWFuO1xuXHRzcWw6IHN0cmluZztcbn07XG5cbmludGVyZmFjZSBPcGVuUXVlcnkge1xuXHRxdWVyeTogbWMuQ29ubmVjdG9yUXVlcnk7XG5cdHN0YXJ0VGltZTogbnVtYmVyO1xuXHRyZXNvbHZlOiAoeDogYXJyb3cuVGFibGUgfCBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT4gdm9pZDtcblx0cmVqZWN0OiAoZXJyPzogc3RyaW5nKSA9PiB2b2lkO1xufVxuXG5leHBvcnQgZGVmYXVsdCAoKSA9PiB7XG5cdGxldCBjb29yZGluYXRvciA9IG5ldyBtYy5Db29yZGluYXRvcigpO1xuXHRsZXQgc2NoZW1hOiBhcnJvdy5TY2hlbWE7XG5cblx0cmV0dXJuIHtcblx0XHRhc3luYyBpbml0aWFsaXplKHsgbW9kZWwgfTogYXcuSW5pdGlhbGl6ZVByb3BzPE1vZGVsPikge1xuXHRcdFx0bGV0IGxvZ2dlciA9IGNvb3JkaW5hdG9yLmxvZ2dlcihfdm9pZExvZ2dlcigpKTtcblx0XHRcdGxldCBvcGVuUXVlcmllcyA9IG5ldyBNYXA8c3RyaW5nLCBPcGVuUXVlcnk+KCk7XG5cblx0XHRcdC8qKlxuXHRcdFx0ICogQHBhcmFtIHF1ZXJ5IC0gdGhlIHF1ZXJ5IHRvIHNlbmRcblx0XHRcdCAqIEBwYXJhbSByZXNvbHZlIC0gdGhlIHByb21pc2UgcmVzb2x2ZSBjYWxsYmFja1xuXHRcdFx0ICogQHBhcmFtIHJlamVjdCAtIHRoZSBwcm9taXNlIHJlamVjdCBjYWxsYmFja1xuXHRcdFx0ICovXG5cdFx0XHRmdW5jdGlvbiBzZW5kKFxuXHRcdFx0XHRxdWVyeTogbWMuQ29ubmVjdG9yUXVlcnksXG5cdFx0XHRcdHJlc29sdmU6ICh2YWx1ZTogYXJyb3cuVGFibGUgfCBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT4gdm9pZCxcblx0XHRcdFx0cmVqZWN0OiAocmVhc29uPzogc3RyaW5nKSA9PiB2b2lkLFxuXHRcdFx0KSB7XG5cdFx0XHRcdGxldCBpZCA9IHV1aWQudjQoKTtcblx0XHRcdFx0b3BlblF1ZXJpZXMuc2V0KGlkLCB7XG5cdFx0XHRcdFx0cXVlcnksXG5cdFx0XHRcdFx0c3RhcnRUaW1lOiBwZXJmb3JtYW5jZS5ub3coKSxcblx0XHRcdFx0XHRyZXNvbHZlLFxuXHRcdFx0XHRcdHJlamVjdCxcblx0XHRcdFx0fSk7XG5cdFx0XHRcdG1vZGVsLnNlbmQoeyAuLi5xdWVyeSwgdXVpZDogaWQgfSk7XG5cdFx0XHR9XG5cblx0XHRcdG1vZGVsLm9uKFwibXNnOmN1c3RvbVwiLCAobXNnLCBidWZmZXJzKSA9PiB7XG5cdFx0XHRcdGxvZ2dlci5ncm91cChgcXVlcnkgJHttc2cudXVpZH1gKTtcblx0XHRcdFx0bG9nZ2VyLmxvZyhcInJlY2VpdmVkIG1lc3NhZ2VcIiwgbXNnLCBidWZmZXJzKTtcblx0XHRcdFx0bGV0IHF1ZXJ5ID0gb3BlblF1ZXJpZXMuZ2V0KG1zZy51dWlkKTtcblx0XHRcdFx0b3BlblF1ZXJpZXMuZGVsZXRlKG1zZy51dWlkKTtcblx0XHRcdFx0YXNzZXJ0KHF1ZXJ5LCBgTm8gcXVlcnkgZm91bmQgZm9yICR7bXNnLnV1aWR9YCk7XG5cdFx0XHRcdGxvZ2dlci5sb2coXG5cdFx0XHRcdFx0cXVlcnkucXVlcnkudG9TdHJpbmcoKSxcblx0XHRcdFx0XHQocGVyZm9ybWFuY2Uubm93KCkgLSBxdWVyeS5zdGFydFRpbWUpLnRvRml4ZWQoMSksXG5cdFx0XHRcdCk7XG5cdFx0XHRcdGlmIChtc2cuZXJyb3IpIHtcblx0XHRcdFx0XHRxdWVyeS5yZWplY3QobXNnLmVycm9yKTtcblx0XHRcdFx0XHRsb2dnZXIuZXJyb3IobXNnLmVycm9yKTtcblx0XHRcdFx0XHRyZXR1cm47XG5cdFx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdFx0c3dpdGNoIChtc2cudHlwZSkge1xuXHRcdFx0XHRcdFx0Y2FzZSBcImFycm93XCI6IHtcblx0XHRcdFx0XHRcdFx0bGV0IHRhYmxlID0gYXJyb3cudGFibGVGcm9tSVBDKGJ1ZmZlcnNbMF0uYnVmZmVyKTtcblx0XHRcdFx0XHRcdFx0bG9nZ2VyLmxvZyhcInRhYmxlXCIsIHRhYmxlKTtcblx0XHRcdFx0XHRcdFx0cXVlcnkucmVzb2x2ZSh0YWJsZSk7XG5cdFx0XHRcdFx0XHRcdGJyZWFrO1xuXHRcdFx0XHRcdFx0fVxuXHRcdFx0XHRcdFx0Y2FzZSBcImpzb25cIjoge1xuXHRcdFx0XHRcdFx0XHRsb2dnZXIubG9nKFwianNvblwiLCBtc2cucmVzdWx0KTtcblx0XHRcdFx0XHRcdFx0cXVlcnkucmVzb2x2ZShtc2cucmVzdWx0KTtcblx0XHRcdFx0XHRcdFx0YnJlYWs7XG5cdFx0XHRcdFx0XHR9XG5cdFx0XHRcdFx0XHRkZWZhdWx0OiB7XG5cdFx0XHRcdFx0XHRcdHF1ZXJ5LnJlc29sdmUoe30pO1xuXHRcdFx0XHRcdFx0XHRicmVhaztcblx0XHRcdFx0XHRcdH1cblx0XHRcdFx0XHR9XG5cdFx0XHRcdH1cblx0XHRcdFx0bG9nZ2VyLmdyb3VwRW5kKFwicXVlcnlcIik7XG5cdFx0XHR9KTtcblxuXHRcdFx0Y29vcmRpbmF0b3IuZGF0YWJhc2VDb25uZWN0b3Ioe1xuXHRcdFx0XHRxdWVyeShxdWVyeSkge1xuXHRcdFx0XHRcdGxldCB7IHByb21pc2UsIHJlc29sdmUsIHJlamVjdCB9ID0gZGVmZXI8XG5cdFx0XHRcdFx0XHRhcnJvdy5UYWJsZSB8IFJlY29yZDxzdHJpbmcsIHVua25vd24+LFxuXHRcdFx0XHRcdFx0c3RyaW5nXG5cdFx0XHRcdFx0PigpO1xuXHRcdFx0XHRcdHNlbmQocXVlcnksIHJlc29sdmUsIHJlamVjdCk7XG5cdFx0XHRcdFx0cmV0dXJuIHByb21pc2U7XG5cdFx0XHRcdH0sXG5cdFx0XHR9KTtcblxuXHRcdFx0Ly8gZ2V0IHNvbWUgaW5pdGlhbCBkYXRhIHRvIGdldCB0aGUgc2NoZW1hXG5cdFx0XHRsZXQgZW1wdHkgPSBhd2FpdCBjb29yZGluYXRvci5xdWVyeShcblx0XHRcdFx0UXVlcnlcblx0XHRcdFx0XHQuZnJvbShtb2RlbC5nZXQoXCJfdGFibGVfbmFtZVwiKSlcblx0XHRcdFx0XHQuc2VsZWN0KC4uLm1vZGVsLmdldChcIl9jb2x1bW5zXCIpKVxuXHRcdFx0XHRcdC5saW1pdCgwKVxuXHRcdFx0XHRcdC50b1N0cmluZygpLFxuXHRcdFx0KTtcblx0XHRcdHNjaGVtYSA9IGVtcHR5LnNjaGVtYTtcblxuXHRcdFx0cmV0dXJuICgpID0+IHtcblx0XHRcdFx0Y29vcmRpbmF0b3IuY2xlYXIoKTtcblx0XHRcdH07XG5cdFx0fSxcblx0XHRyZW5kZXIoeyBtb2RlbCwgZWwgfTogYXcuUmVuZGVyUHJvcHM8TW9kZWw+KSB7XG5cdFx0XHRsZXQgdGFibGUgPSBuZXcgRGF0YVRhYmxlKHtcblx0XHRcdFx0dGFibGU6IG1vZGVsLmdldChcIl90YWJsZV9uYW1lXCIpLFxuXHRcdFx0XHRzY2hlbWE6IHNjaGVtYSxcblx0XHRcdH0pO1xuXHRcdFx0Y29vcmRpbmF0b3IuY29ubmVjdCh0YWJsZSk7XG5cdFx0XHRlZmZlY3QoKCkgPT4ge1xuXHRcdFx0XHRtb2RlbC5zZXQoXCJzcWxcIiwgdGFibGUuc3FsID8/IFwiXCIpO1xuXHRcdFx0XHRtb2RlbC5zYXZlX2NoYW5nZXMoKTtcblx0XHRcdH0pO1xuXHRcdFx0ZWwuYXBwZW5kQ2hpbGQodGFibGUubm9kZSgpKTtcblx0XHR9LFxuXHR9O1xufTtcblxuZnVuY3Rpb24gX3ZvaWRMb2dnZXIoKSB7XG5cdHJldHVybiBPYmplY3QuZnJvbUVudHJpZXMoXG5cdFx0T2JqZWN0LmtleXMoY29uc29sZSkubWFwKChrZXkpID0+IFtrZXksICgpID0+IHt9XSksXG5cdCk7XG59XG4iLCAiaW1wb3J0ICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuLy8gQGRlbm8tdHlwZXM9XCIuLi9kZXBzL21vc2FpYy1jb3JlLmQudHNcIlxuaW1wb3J0IHtcblx0Q29vcmRpbmF0b3IsXG5cdHR5cGUgRmllbGRJbmZvLFxuXHR0eXBlIEZpZWxkUmVxdWVzdCxcblx0TW9zYWljQ2xpZW50LFxuXHRTZWxlY3Rpb24sXG59IGZyb20gXCJAdXdkYXRhL21vc2FpYy1jb3JlXCI7XG4vLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLXNxbC5kLnRzXCJcbmltcG9ydCB7IGRlc2MsIFF1ZXJ5LCBTUUxFeHByZXNzaW9uIH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuaW1wb3J0ICogYXMgc2lnbmFscyBmcm9tIFwiQHByZWFjdC9zaWduYWxzLWNvcmVcIjtcbmltcG9ydCB7IGh0bWwgfSBmcm9tIFwiaHRsXCI7XG5cbmltcG9ydCB7IEFzeW5jQmF0Y2hSZWFkZXIgfSBmcm9tIFwiLi4vdXRpbHMvQXN5bmNCYXRjaFJlYWRlci50c1wiO1xuaW1wb3J0IHsgYXNzZXJ0IH0gZnJvbSBcIi4uL3V0aWxzL2Fzc2VydC50c1wiO1xuaW1wb3J0IHsgZm9ybWF0RGF0YVR5cGUsIGZvcm1hdHRlckZvclZhbHVlIH0gZnJvbSBcIi4uL3V0aWxzL2Zvcm1hdHRpbmcudHNcIjtcbmltcG9ydCB7IEhpc3RvZ3JhbSB9IGZyb20gXCIuL0hpc3RvZ3JhbS50c1wiO1xuaW1wb3J0IHsgVmFsdWVDb3VudHMgfSBmcm9tIFwiLi9WYWx1ZUNvdW50cy50c1wiO1xuaW1wb3J0IHsgc2lnbmFsIH0gZnJvbSBcIkBwcmVhY3Qvc2lnbmFscy1jb3JlXCI7XG5cbmltcG9ydCBzdHlsZXNTdHJpbmcgZnJvbSBcIi4vc3R5bGVzLmNzcz9yYXdcIjtcbmltcG9ydCB7IFN0YXR1c0JhciB9IGZyb20gXCIuL1N0YXR1c0Jhci50c1wiO1xuXG5pbnRlcmZhY2UgRGF0YVRhYmxlT3B0aW9ucyB7XG5cdHRhYmxlOiBzdHJpbmc7XG5cdHNjaGVtYTogYXJyb3cuU2NoZW1hO1xuXHRoZWlnaHQ/OiBudW1iZXI7XG59XG5cbi8vIFRPRE86IG1vcmVcbnR5cGUgQ29sdW1uU3VtbWFyeUNsaWVudCA9IEhpc3RvZ3JhbSB8IFZhbHVlQ291bnRzO1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gZGF0YXRhYmxlKFxuXHR0YWJsZTogc3RyaW5nLFxuXHRvcHRpb25zOiB7XG5cdFx0Y29vcmRpbmF0b3I/OiBDb29yZGluYXRvcjtcblx0XHRoZWlnaHQ/OiBudW1iZXI7XG5cdFx0Y29sdW1ucz86IEFycmF5PHN0cmluZz47XG5cdH0gPSB7fSxcbikge1xuXHRhc3NlcnQob3B0aW9ucy5jb29yZGluYXRvciwgXCJNdXN0IHByb3ZpZGUgYSBjb29yZGluYXRvclwiKTtcblx0bGV0IGVtcHR5ID0gYXdhaXQgb3B0aW9ucy5jb29yZGluYXRvci5xdWVyeShcblx0XHRRdWVyeVxuXHRcdFx0LmZyb20odGFibGUpXG5cdFx0XHQuc2VsZWN0KG9wdGlvbnMuY29sdW1ucyA/PyBbXCIqXCJdKVxuXHRcdFx0LmxpbWl0KDApXG5cdFx0XHQudG9TdHJpbmcoKSxcblx0KTtcblx0bGV0IGNsaWVudCA9IG5ldyBEYXRhVGFibGUoe1xuXHRcdHRhYmxlLFxuXHRcdHNjaGVtYTogZW1wdHkuc2NoZW1hLFxuXHRcdGhlaWdodDogb3B0aW9ucy5oZWlnaHQsXG5cdH0pO1xuXHRvcHRpb25zLmNvb3JkaW5hdG9yLmNvbm5lY3QoY2xpZW50KTtcblx0cmV0dXJuIGNsaWVudDtcbn1cblxuZXhwb3J0IGNsYXNzIERhdGFUYWJsZSBleHRlbmRzIE1vc2FpY0NsaWVudCB7XG5cdC8qKiBzb3VyY2Ugb2YgdGhlIGRhdGEgKi9cblx0I21ldGE6IHsgdGFibGU6IHN0cmluZzsgc2NoZW1hOiBhcnJvdy5TY2hlbWEgfTtcblx0LyoqIGZvciB0aGUgY29tcG9uZW50ICovXG5cdCNyb290OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdC8qKiBzaGFkb3cgcm9vdCBmb3IgdGhlIGNvbXBvbmVudCAqL1xuXHQjc2hhZG93Um9vdDogU2hhZG93Um9vdCA9IHRoaXMuI3Jvb3QuYXR0YWNoU2hhZG93KHsgbW9kZTogXCJvcGVuXCIgfSk7XG5cdC8qKiBoZWFkZXIgb2YgdGhlIHRhYmxlICovXG5cdCN0aGVhZDogSFRNTFRhYmxlU2VjdGlvbkVsZW1lbnQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwidGhlYWRcIik7XG5cdC8qKiBib2R5IG9mIHRoZSB0YWJsZSAqL1xuXHQjdGJvZHk6IEhUTUxUYWJsZVNlY3Rpb25FbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInRib2R5XCIpO1xuXHQvKiogVGhlIFNRTCBvcmRlciBieSAqL1xuXHQjb3JkZXJieTogQXJyYXk8eyBmaWVsZDogc3RyaW5nOyBvcmRlcjogXCJhc2NcIiB8IFwiZGVzY1wiIHwgXCJ1bnNldFwiIH0+ID0gW107XG5cdC8qKiB0ZW1wbGF0ZSByb3cgZm9yIGRhdGEgKi9cblx0I3RlbXBsYXRlUm93OiBIVE1MVGFibGVSb3dFbGVtZW50IHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkO1xuXHQvKiogZGl2IGNvbnRhaW5pbmcgdGhlIHRhYmxlICovXG5cdCN0YWJsZVJvb3Q6IEhUTUxEaXZFbGVtZW50O1xuXHQvKiogb2Zmc2V0IGludG8gdGhlIGRhdGEgKi9cblx0I29mZnNldDogbnVtYmVyID0gMDtcblx0LyoqIG51bWJlciBvZiByb3dzIHRvIGZldGNoICovXG5cdCNsaW1pdDogbnVtYmVyID0gMTAwO1xuXHQvKiogd2hldGhlciBhbiBpbnRlcm5hbCByZXF1ZXN0IGlzIHBlbmRpbmcgKi9cblx0I3BlbmRpbmdJbnRlcm5hbFJlcXVlc3Q6IGJvb2xlYW4gPSB0cnVlO1xuXHQvKiogbnVtYmVyIG9mIHJvd3MgdG8gZGlzcGxheSAqL1xuXHQjcm93czogbnVtYmVyID0gMTEuNTtcblx0LyoqIGhlaWdodCBvZiBhIHJvdyAqL1xuXHQjcm93SGVpZ2h0OiBudW1iZXIgPSAyMjtcblx0LyoqIHdpZHRoIG9mIGEgY29sdW1uICovXG5cdCNjb2x1bW5XaWR0aDogbnVtYmVyID0gMTI1O1xuXHQvKiogaGVpZ2h0IG9mIHRoZSBoZWFkZXIgKi9cblx0I2hlYWRlckhlaWdodDogc3RyaW5nID0gXCI5NHB4XCI7XG5cdC8qKiB0aGUgZm9ybWF0dGVyIGZvciB0aGUgZGF0YSB0YWJsZSBlbnRyaWVzICovXG5cdCNmb3JtYXQ6IFJlY29yZDxzdHJpbmcsICh2YWx1ZTogdW5rbm93bikgPT4gc3RyaW5nPjtcblxuXHQvKiogQHR5cGUge0FzeW5jQmF0Y2hSZWFkZXI8YXJyb3cuU3RydWN0Um93UHJveHk+IHwgbnVsbH0gKi9cblx0I3JlYWRlcjogQXN5bmNCYXRjaFJlYWRlcjxhcnJvdy5TdHJ1Y3RSb3dQcm94eT4gfCBudWxsID0gbnVsbDtcblxuXHQjc3FsID0gc2lnbmFsKHVuZGVmaW5lZCBhcyBzdHJpbmcgfCB1bmRlZmluZWQpO1xuXG5cdGNvbnN0cnVjdG9yKHNvdXJjZTogRGF0YVRhYmxlT3B0aW9ucykge1xuXHRcdHN1cGVyKFNlbGVjdGlvbi5jcm9zc2ZpbHRlcigpKTtcblx0XHR0aGlzLiNmb3JtYXQgPSBmb3JtYXRvZihzb3VyY2Uuc2NoZW1hKTtcblx0XHR0aGlzLiNtZXRhID0gc291cmNlO1xuXG5cdFx0bGV0IG1heEhlaWdodCA9IGAkeyh0aGlzLiNyb3dzICsgMSkgKiB0aGlzLiNyb3dIZWlnaHQgLSAxfXB4YDtcblx0XHQvLyBpZiBtYXhIZWlnaHQgaXMgc2V0LCBjYWxjdWxhdGUgdGhlIG51bWJlciBvZiByb3dzIHRvIGRpc3BsYXlcblx0XHRpZiAoc291cmNlLmhlaWdodCkge1xuXHRcdFx0dGhpcy4jcm93cyA9IE1hdGguZmxvb3Ioc291cmNlLmhlaWdodCAvIHRoaXMuI3Jvd0hlaWdodCk7XG5cdFx0XHRtYXhIZWlnaHQgPSBgJHtzb3VyY2UuaGVpZ2h0fXB4YDtcblx0XHR9XG5cblx0XHRsZXQgcm9vdDogSFRNTERpdkVsZW1lbnQgPSBodG1sYDxkaXYgY2xhc3M9XCJxdWFrXCIgc3R5bGU9JHt7XG5cdFx0XHRtYXhIZWlnaHQsXG5cdFx0fX0+YDtcblx0XHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdFx0cm9vdC5hcHBlbmRDaGlsZChcblx0XHRcdGh0bWwuZnJhZ21lbnRgPHRhYmxlIHN0eWxlPSR7eyB0YWJsZUxheW91dDogXCJmaXhlZFwiIH19PiR7dGhpcy4jdGhlYWR9JHt0aGlzLiN0Ym9keX08L3RhYmxlPmBcblx0XHQpO1xuXHRcdHRoaXMuI3NoYWRvd1Jvb3QuYXBwZW5kQ2hpbGQoaHRtbGA8c3R5bGU+JHtzdHlsZXNTdHJpbmd9PC9zdHlsZT5gKTtcblx0XHR0aGlzLiNzaGFkb3dSb290LmFwcGVuZENoaWxkKHJvb3QpO1xuXHRcdHRoaXMuI3RhYmxlUm9vdCA9IHJvb3Q7XG5cblx0XHRhZGREaXJlY3Rpb25hbFNjcm9sbFdpdGhQcmV2ZW50RGVmYXVsdCh0aGlzLiN0YWJsZVJvb3QpO1xuXG5cdFx0Ly8gc2Nyb2xsIGV2ZW50IGxpc3RlbmVyXG5cdFx0dGhpcy4jdGFibGVSb290LmFkZEV2ZW50TGlzdGVuZXIoXCJzY3JvbGxcIiwgYXN5bmMgKCkgPT4ge1xuXHRcdFx0bGV0IGlzQXRCb3R0b20gPVxuXHRcdFx0XHR0aGlzLiN0YWJsZVJvb3Quc2Nyb2xsSGVpZ2h0IC0gdGhpcy4jdGFibGVSb290LnNjcm9sbFRvcCA8XG5cdFx0XHRcdFx0dGhpcy4jcm93cyAqIHRoaXMuI3Jvd0hlaWdodCAqIDEuNTtcblx0XHRcdGlmIChpc0F0Qm90dG9tKSB7XG5cdFx0XHRcdGF3YWl0IHRoaXMuI2FwcGVuZFJvd3ModGhpcy4jcm93cyk7XG5cdFx0XHR9XG5cdFx0fSk7XG5cdH1cblxuXHRnZXQgc3FsKCkge1xuXHRcdHJldHVybiB0aGlzLiNzcWwudmFsdWU7XG5cdH1cblxuXHRmaWVsZHMoKTogQXJyYXk8RmllbGRSZXF1ZXN0PiB7XG5cdFx0cmV0dXJuIHRoaXMuI2NvbHVtbnMubWFwKChjb2x1bW4pID0+ICh7XG5cdFx0XHR0YWJsZTogdGhpcy4jbWV0YS50YWJsZSxcblx0XHRcdGNvbHVtbixcblx0XHRcdHN0YXRzOiBbXSxcblx0XHR9KSk7XG5cdH1cblxuXHRub2RlKCkge1xuXHRcdHJldHVybiB0aGlzLiNyb290O1xuXHR9XG5cblx0cmVzaXplKGhlaWdodDogbnVtYmVyKSB7XG5cdFx0dGhpcy4jcm93cyA9IE1hdGguZmxvb3IoaGVpZ2h0IC8gdGhpcy4jcm93SGVpZ2h0KTtcblx0XHR0aGlzLiN0YWJsZVJvb3Quc3R5bGUubWF4SGVpZ2h0ID0gYCR7aGVpZ2h0fXB4YDtcblx0XHR0aGlzLiN0YWJsZVJvb3Quc2Nyb2xsVG9wID0gMDtcblx0fVxuXG5cdGdldCAjY29sdW1ucygpIHtcblx0XHRyZXR1cm4gdGhpcy4jbWV0YS5zY2hlbWEuZmllbGRzLm1hcCgoZmllbGQpID0+IGZpZWxkLm5hbWUpO1xuXHR9XG5cblx0LyoqXG5cdCAqIEBwYXJhbSB7QXJyYXk8dW5rbm93bj59IGZpbHRlclxuXHQgKi9cblx0cXVlcnkoZmlsdGVyOiBBcnJheTx1bmtub3duPiA9IFtdKSB7XG5cdFx0bGV0IHF1ZXJ5ID0gUXVlcnkuZnJvbSh0aGlzLiNtZXRhLnRhYmxlKVxuXHRcdFx0LnNlbGVjdCh0aGlzLiNjb2x1bW5zKVxuXHRcdFx0LndoZXJlKGZpbHRlcilcblx0XHRcdC5vcmRlcmJ5KFxuXHRcdFx0XHR0aGlzLiNvcmRlcmJ5XG5cdFx0XHRcdFx0LmZpbHRlcigobykgPT4gby5vcmRlciAhPT0gXCJ1bnNldFwiKVxuXHRcdFx0XHRcdC5tYXAoKG8pID0+IG8ub3JkZXIgPT09IFwiYXNjXCIgPyBhc2Moby5maWVsZCkgOiBkZXNjKG8uZmllbGQpKSxcblx0XHRcdCk7XG5cdFx0dGhpcy4jc3FsLnZhbHVlID0gcXVlcnkuY2xvbmUoKS50b1N0cmluZygpO1xuXHRcdHJldHVybiBxdWVyeVxuXHRcdFx0LmxpbWl0KHRoaXMuI2xpbWl0KVxuXHRcdFx0Lm9mZnNldCh0aGlzLiNvZmZzZXQpO1xuXHR9XG5cblx0LyoqXG5cdCAqIEEgbW9zaWFjIGxpZmVjeWNsZSBmdW5jdGlvbiB0aGF0IGlzIGNhbGxlZCB3aXRoIHRoZSByZXN1bHRzIGZyb20gYHF1ZXJ5YC5cblx0ICogTXVzdCBiZSBzeW5jaHJvbm91cywgYW5kIHJldHVybiBgdGhpc2AuXG5cdCAqL1xuXHRxdWVyeVJlc3VsdCh0YWJsZTogYXJyb3cuVGFibGUpIHtcblx0XHRpZiAoIXRoaXMuI3BlbmRpbmdJbnRlcm5hbFJlcXVlc3QpIHtcblx0XHRcdC8vIGRhdGEgaXMgbm90IGZyb20gYW4gaW50ZXJuYWwgcmVxdWVzdCwgc28gcmVzZXQgdGFibGVcblx0XHRcdHRoaXMuI3JlYWRlciA9IG5ldyBBc3luY0JhdGNoUmVhZGVyKCgpID0+IHtcblx0XHRcdFx0dGhpcy4jcGVuZGluZ0ludGVybmFsUmVxdWVzdCA9IHRydWU7XG5cdFx0XHRcdHRoaXMucmVxdWVzdERhdGEodGhpcy4jb2Zmc2V0ICsgdGhpcy4jbGltaXQpO1xuXHRcdFx0fSk7XG5cdFx0XHR0aGlzLiN0Ym9keS5yZXBsYWNlQ2hpbGRyZW4oKTtcblx0XHRcdHRoaXMuI3RhYmxlUm9vdC5zY3JvbGxUb3AgPSAwO1xuXHRcdFx0dGhpcy4jb2Zmc2V0ID0gMDtcblx0XHR9XG5cdFx0bGV0IGJhdGNoID0gdGFibGVbU3ltYm9sLml0ZXJhdG9yXSgpO1xuXHRcdHRoaXMuI3JlYWRlcj8uZW5xdWV1ZUJhdGNoKGJhdGNoLCB7XG5cdFx0XHRsYXN0OiB0YWJsZS5udW1Sb3dzIDwgdGhpcy4jbGltaXQsXG5cdFx0fSk7XG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHR1cGRhdGUoKSB7XG5cdFx0aWYgKCF0aGlzLiNwZW5kaW5nSW50ZXJuYWxSZXF1ZXN0KSB7XG5cdFx0XHQvLyBvbiB0aGUgZmlyc3QgdXBkYXRlLCBwb3B1bGF0ZSB0aGUgdGFibGUgd2l0aCBpbml0aWFsIGRhdGFcblx0XHRcdHRoaXMuI2FwcGVuZFJvd3ModGhpcy4jcm93cyAqIDIpO1xuXHRcdH1cblx0XHR0aGlzLiNwZW5kaW5nSW50ZXJuYWxSZXF1ZXN0ID0gZmFsc2U7XG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHRyZXF1ZXN0RGF0YShvZmZzZXQgPSAwKSB7XG5cdFx0dGhpcy4jb2Zmc2V0ID0gb2Zmc2V0O1xuXG5cdFx0Ly8gcmVxdWVzdCBuZXh0IGRhdGEgYmF0Y2hcblx0XHRsZXQgcXVlcnkgPSB0aGlzLnF1ZXJ5KHRoaXMuZmlsdGVyQnk/LnByZWRpY2F0ZSh0aGlzKSk7XG5cdFx0dGhpcy5yZXF1ZXN0UXVlcnkocXVlcnkpO1xuXG5cdFx0Ly8gcHJlZmV0Y2ggc3Vic2VxdWVudCBkYXRhIGJhdGNoXG5cdFx0dGhpcy5jb29yZGluYXRvci5wcmVmZXRjaChxdWVyeS5jbG9uZSgpLm9mZnNldChvZmZzZXQgKyB0aGlzLiNsaW1pdCkpO1xuXHR9XG5cblx0ZmllbGRJbmZvKGluZm9zOiBBcnJheTxGaWVsZEluZm8+KSB7XG5cdFx0bGV0IGNsYXNzZXMgPSBjbGFzc29mKHRoaXMuI21ldGEuc2NoZW1hKTtcblxuXHRcdHtcblx0XHRcdGxldCBzdGF0dXNCYXIgPSBuZXcgU3RhdHVzQmFyKHtcblx0XHRcdFx0dGFibGU6IHRoaXMuI21ldGEudGFibGUsXG5cdFx0XHRcdGZpbHRlckJ5OiB0aGlzLmZpbHRlckJ5LFxuXHRcdFx0fSk7XG5cdFx0XHR0aGlzLmNvb3JkaW5hdG9yLmNvbm5lY3Qoc3RhdHVzQmFyKTtcblx0XHRcdHRoaXMuI3NoYWRvd1Jvb3QuYXBwZW5kQ2hpbGQoc3RhdHVzQmFyLm5vZGUoKSk7XG5cdFx0fVxuXG5cdFx0Ly8gQGRlbm8tZm10LWlnbm9yZVxuXHRcdHRoaXMuI3RlbXBsYXRlUm93ID0gaHRtbGA8dHI+PHRkPjwvdGQ+JHtcblx0XHRcdGluZm9zLm1hcCgoaW5mbykgPT4gaHRtbC5mcmFnbWVudGA8dGQgY2xhc3M9JHtjbGFzc2VzW2luZm8uY29sdW1uXX0+PC90ZD5gKVxuXHRcdH1cblx0XHRcdDx0ZCBzdHlsZT0ke3sgd2lkdGg6IFwiOTklXCIsIGJvcmRlckxlZnQ6IFwibm9uZVwiLCBib3JkZXJSaWdodDogXCJub25lXCIgfX0+PC90ZD5cblx0XHQ8L3RyPmA7XG5cblx0XHRsZXQgb2JzZXJ2ZXIgPSBuZXcgSW50ZXJzZWN0aW9uT2JzZXJ2ZXIoKGVudHJpZXMpID0+IHtcblx0XHRcdGZvciAobGV0IGVudHJ5IG9mIGVudHJpZXMpIHtcblx0XHRcdFx0aWYgKCFpc1RhYmxlQ29sdW1uSGVhZGVyV2l0aFN2ZyhlbnRyeS50YXJnZXQpKSBjb250aW51ZTtcblx0XHRcdFx0bGV0IHZpcyA9IGVudHJ5LnRhcmdldC52aXM7XG5cdFx0XHRcdGlmICghdmlzKSBjb250aW51ZTtcblx0XHRcdFx0aWYgKGVudHJ5LmlzSW50ZXJzZWN0aW5nKSB7XG5cdFx0XHRcdFx0dGhpcy5jb29yZGluYXRvci5jb25uZWN0KHZpcyk7XG5cdFx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdFx0dGhpcy5jb29yZGluYXRvcj8uZGlzY29ubmVjdCh2aXMpO1xuXHRcdFx0XHR9XG5cdFx0XHR9XG5cdFx0fSwge1xuXHRcdFx0cm9vdDogdGhpcy4jdGFibGVSb290LFxuXHRcdH0pO1xuXG5cdFx0bGV0IGNvbHMgPSB0aGlzLiNtZXRhLnNjaGVtYS5maWVsZHMubWFwKChmaWVsZCkgPT4ge1xuXHRcdFx0bGV0IGluZm8gPSBpbmZvcy5maW5kKChjKSA9PiBjLmNvbHVtbiA9PT0gZmllbGQubmFtZSk7XG5cdFx0XHRhc3NlcnQoaW5mbywgYE5vIGluZm8gZm9yIGNvbHVtbiAke2ZpZWxkLm5hbWV9YCk7XG5cdFx0XHRsZXQgdmlzOiBDb2x1bW5TdW1tYXJ5Q2xpZW50IHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkO1xuXHRcdFx0aWYgKGluZm8udHlwZSA9PT0gXCJudW1iZXJcIiB8fCBpbmZvLnR5cGUgPT09IFwiZGF0ZVwiKSB7XG5cdFx0XHRcdHZpcyA9IG5ldyBIaXN0b2dyYW0oe1xuXHRcdFx0XHRcdHRhYmxlOiB0aGlzLiNtZXRhLnRhYmxlLFxuXHRcdFx0XHRcdGNvbHVtbjogZmllbGQubmFtZSxcblx0XHRcdFx0XHR0eXBlOiBpbmZvLnR5cGUsXG5cdFx0XHRcdFx0ZmlsdGVyQnk6IHRoaXMuZmlsdGVyQnkhLFxuXHRcdFx0XHR9KTtcblx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdHZpcyA9IG5ldyBWYWx1ZUNvdW50cyh7XG5cdFx0XHRcdFx0dGFibGU6IHRoaXMuI21ldGEudGFibGUsXG5cdFx0XHRcdFx0Y29sdW1uOiBmaWVsZC5uYW1lLFxuXHRcdFx0XHRcdGZpbHRlckJ5OiB0aGlzLmZpbHRlckJ5ISxcblx0XHRcdFx0fSk7XG5cdFx0XHR9XG5cdFx0XHRsZXQgdGggPSB0aGNvbChmaWVsZCwgdGhpcy4jY29sdW1uV2lkdGgsIHZpcyk7XG5cdFx0XHRvYnNlcnZlci5vYnNlcnZlKHRoKTtcblx0XHRcdHJldHVybiB0aDtcblx0XHR9KTtcblxuXHRcdHNpZ25hbHMuZWZmZWN0KCgpID0+IHtcblx0XHRcdHRoaXMuI29yZGVyYnkgPSBjb2xzLm1hcCgoY29sLCBpKSA9PiAoe1xuXHRcdFx0XHRmaWVsZDogdGhpcy4jY29sdW1uc1tpXSxcblx0XHRcdFx0b3JkZXI6IGNvbC5zb3J0U3RhdGUudmFsdWUsXG5cdFx0XHR9KSk7XG5cdFx0XHR0aGlzLnJlcXVlc3REYXRhKCk7XG5cdFx0fSk7XG5cblx0XHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdFx0dGhpcy4jdGhlYWQuYXBwZW5kQ2hpbGQoXG5cdFx0XHRodG1sYDx0ciBzdHlsZT0ke3sgaGVpZ2h0OiB0aGlzLiNoZWFkZXJIZWlnaHQgfX0+XG5cdFx0XHRcdDx0aD48L3RoPlxuXHRcdFx0XHQke2NvbHN9XG5cdFx0XHRcdDx0aCBzdHlsZT0ke3sgd2lkdGg6IFwiOTklXCIsIGJvcmRlckxlZnQ6IFwibm9uZVwiLCBib3JkZXJSaWdodDogXCJub25lXCIgfX0+PC90aD5cblx0XHRcdDwvdHI+YCxcblx0XHQpO1xuXG5cdFx0Ly8gaGlnaGxpZ2h0IG9uIGhvdmVyXG5cdFx0e1xuXHRcdFx0dGhpcy4jdGFibGVSb290LmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZW92ZXJcIiwgKGV2ZW50KSA9PiB7XG5cdFx0XHRcdGlmIChcblx0XHRcdFx0XHRpc1RhYmxlQ2VsbEVsZW1lbnQoZXZlbnQudGFyZ2V0KSAmJlxuXHRcdFx0XHRcdGlzVGFibGVSb3dFbGVtZW50KGV2ZW50LnRhcmdldC5wYXJlbnROb2RlKVxuXHRcdFx0XHQpIHtcblx0XHRcdFx0XHRjb25zdCBjZWxsID0gZXZlbnQudGFyZ2V0O1xuXHRcdFx0XHRcdGNvbnN0IHJvdyA9IGV2ZW50LnRhcmdldC5wYXJlbnROb2RlO1xuXHRcdFx0XHRcdGhpZ2hsaWdodChjZWxsLCByb3cpO1xuXHRcdFx0XHR9XG5cdFx0XHR9KTtcblx0XHRcdHRoaXMuI3RhYmxlUm9vdC5hZGRFdmVudExpc3RlbmVyKFwibW91c2VvdXRcIiwgKGV2ZW50KSA9PiB7XG5cdFx0XHRcdGlmIChcblx0XHRcdFx0XHRpc1RhYmxlQ2VsbEVsZW1lbnQoZXZlbnQudGFyZ2V0KSAmJlxuXHRcdFx0XHRcdGlzVGFibGVSb3dFbGVtZW50KGV2ZW50LnRhcmdldC5wYXJlbnROb2RlKVxuXHRcdFx0XHQpIHtcblx0XHRcdFx0XHRjb25zdCBjZWxsID0gZXZlbnQudGFyZ2V0O1xuXHRcdFx0XHRcdGNvbnN0IHJvdyA9IGV2ZW50LnRhcmdldC5wYXJlbnROb2RlO1xuXHRcdFx0XHRcdHJlbW92ZUhpZ2hsaWdodChjZWxsLCByb3cpO1xuXHRcdFx0XHR9XG5cdFx0XHR9KTtcblx0XHR9XG5cblx0XHRyZXR1cm4gdGhpcztcblx0fVxuXG5cdC8qKiBOdW1iZXIgb2Ygcm93cyB0byBhcHBlbmQgKi9cblx0YXN5bmMgI2FwcGVuZFJvd3MobnJvd3M6IG51bWJlcikge1xuXHRcdG5yb3dzID0gTWF0aC50cnVuYyhucm93cyk7XG5cdFx0d2hpbGUgKG5yb3dzID49IDApIHtcblx0XHRcdGxldCByZXN1bHQgPSBhd2FpdCB0aGlzLiNyZWFkZXI/Lm5leHQoKTtcblx0XHRcdGlmICghcmVzdWx0IHx8IHJlc3VsdD8uZG9uZSkge1xuXHRcdFx0XHQvLyB3ZSd2ZSBleGhhdXN0ZWQgYWxsIHJvd3Ncblx0XHRcdFx0YnJlYWs7XG5cdFx0XHR9XG5cdFx0XHR0aGlzLiNhcHBlbmRSb3cocmVzdWx0LnZhbHVlLnJvdywgcmVzdWx0LnZhbHVlLmluZGV4KTtcblx0XHRcdG5yb3dzLS07XG5cdFx0XHRjb250aW51ZTtcblx0XHR9XG5cdH1cblxuXHQjYXBwZW5kUm93KGQ6IGFycm93LlN0cnVjdFJvd1Byb3h5LCBpOiBudW1iZXIpIHtcblx0XHRsZXQgaXRyID0gdGhpcy4jdGVtcGxhdGVSb3c/LmNsb25lTm9kZSh0cnVlKTtcblx0XHRhc3NlcnQoaXRyLCBcIk11c3QgaGF2ZSBhIGRhdGEgcm93XCIpO1xuXHRcdGxldCB0ZCA9IGl0ci5jaGlsZE5vZGVzWzBdIGFzIEhUTUxUYWJsZUNlbGxFbGVtZW50O1xuXHRcdHRkLmFwcGVuZENoaWxkKGRvY3VtZW50LmNyZWF0ZVRleHROb2RlKFN0cmluZyhpKSkpO1xuXHRcdGZvciAobGV0IGogPSAwOyBqIDwgdGhpcy4jY29sdW1ucy5sZW5ndGg7ICsraikge1xuXHRcdFx0dGQgPSBpdHIuY2hpbGROb2Rlc1tqICsgMV0gYXMgSFRNTFRhYmxlQ2VsbEVsZW1lbnQ7XG5cdFx0XHR0ZC5jbGFzc0xpc3QucmVtb3ZlKFwiZ3JheVwiKTtcblx0XHRcdGxldCBjb2wgPSB0aGlzLiNjb2x1bW5zW2pdO1xuXHRcdFx0bGV0IHN0cmluZ2lmaWVkID0gdGhpcy4jZm9ybWF0W2NvbF0oZFtjb2xdKTtcblx0XHRcdGlmIChzaG91bGRHcmF5b3V0VmFsdWUoc3RyaW5naWZpZWQpKSB7XG5cdFx0XHRcdHRkLmNsYXNzTGlzdC5hZGQoXCJncmF5XCIpO1xuXHRcdFx0fVxuXHRcdFx0bGV0IHZhbHVlID0gZG9jdW1lbnQuY3JlYXRlVGV4dE5vZGUoc3RyaW5naWZpZWQpO1xuXHRcdFx0dGQuYXBwZW5kQ2hpbGQodmFsdWUpO1xuXHRcdH1cblx0XHR0aGlzLiN0Ym9keS5hcHBlbmQoaXRyKTtcblx0fVxufVxuXG5jb25zdCBUUlVOQ0FURSA9IC8qKiBAdHlwZSB7Y29uc3R9ICovICh7XG5cdHdoaXRlU3BhY2U6IFwibm93cmFwXCIsXG5cdG92ZXJmbG93OiBcImhpZGRlblwiLFxuXHR0ZXh0T3ZlcmZsb3c6IFwiZWxsaXBzaXNcIixcbn0pO1xuXG5mdW5jdGlvbiB0aGNvbChcblx0ZmllbGQ6IGFycm93LkZpZWxkLFxuXHRtaW5XaWR0aDogbnVtYmVyLFxuXHR2aXM/OiBDb2x1bW5TdW1tYXJ5Q2xpZW50LFxuKSB7XG5cdGxldCBidXR0b25WaXNpYmxlID0gc2lnbmFscy5zaWduYWwoZmFsc2UpO1xuXHRsZXQgd2lkdGggPSBzaWduYWxzLnNpZ25hbChtaW5XaWR0aCk7XG5cdGxldCBzb3J0U3RhdGU6IHNpZ25hbHMuU2lnbmFsPFwidW5zZXRcIiB8IFwiYXNjXCIgfCBcImRlc2NcIj4gPSBzaWduYWxzLnNpZ25hbChcblx0XHRcInVuc2V0XCIsXG5cdCk7XG5cblx0ZnVuY3Rpb24gbmV4dFNvcnRTdGF0ZSgpIHtcblx0XHQvLyBzaW1wbGUgc3RhdGUgbWFjaGluZVxuXHRcdC8vIHVuc2V0IC0+IGFzYyAtPiBkZXNjIC0+IHVuc2V0XG5cdFx0c29ydFN0YXRlLnZhbHVlID0gKHtcblx0XHRcdFwidW5zZXRcIjogXCJhc2NcIixcblx0XHRcdFwiYXNjXCI6IFwiZGVzY1wiLFxuXHRcdFx0XCJkZXNjXCI6IFwidW5zZXRcIixcblx0XHR9IGFzIGNvbnN0KVtzb3J0U3RhdGUudmFsdWVdO1xuXHR9XG5cblx0Ly8gQGRlbm8tZm10LWlnbm9yZVxuXHRsZXQgc3ZnID0gaHRtbGA8c3ZnIHN0eWxlPSR7eyB3aWR0aDogXCIxLjVlbVwiIH19IGZpbGw9XCJub25lXCIgdmlld0JveD1cIjAgMCAyNCAyNFwiIHN0cm9rZS13aWR0aD1cIjEuNVwiIHN0cm9rZT1cImN1cnJlbnRDb2xvclwiPlxuXHRcdDxwYXRoIHN0cm9rZS1saW5lY2FwPVwicm91bmRcIiBzdHJva2UtbGluZWpvaW49XCJyb3VuZFwiIGQ9XCJNOC4yNSA5TDEyIDUuMjVMMTUuNzUgOVwiIC8+XG5cdFx0PHBhdGggc3Ryb2tlLWxpbmVjYXA9XCJyb3VuZFwiIHN0cm9rZS1saW5lam9pbj1cInJvdW5kXCIgZD1cIk04LjI1IDE1TDEyIDE4Ljc1TDE1Ljc1IDE1XCIgLz5cblx0PC9zdmc+YDtcblx0bGV0IHVwYXJyb3c6IFNWR1BhdGhFbGVtZW50ID0gc3ZnLmNoaWxkcmVuWzBdO1xuXHRsZXQgZG93bmFycm93OiBTVkdQYXRoRWxlbWVudCA9IHN2Zy5jaGlsZHJlblsxXTtcblx0bGV0IHZlcnRpY2FsUmVzaXplSGFuZGxlOiBIVE1MRGl2RWxlbWVudCA9XG5cdFx0aHRtbGA8ZGl2IGNsYXNzPVwicmVzaXplLWhhbmRsZVwiPjwvZGl2PmA7XG5cdC8vIEBkZW5vLWZtdC1pZ25vcmVcblx0bGV0IHNvcnRCdXR0b24gPSBodG1sYDxzcGFuIGFyaWEtcm9sZT1cImJ1dHRvblwiIGNsYXNzPVwic29ydC1idXR0b25cIiBvbm1vdXNlZG93bj0ke25leHRTb3J0U3RhdGV9PiR7c3ZnfTwvc3Bhbj5gO1xuXHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdGxldCB0aDogSFRNTFRhYmxlQ2VsbEVsZW1lbnQgPSBodG1sYDx0aCBzdHlsZT0ke3sgb3ZlcmZsb3c6IFwiaGlkZGVuXCIgfX0+XG5cdFx0PGRpdiBzdHlsZT0ke3sgZGlzcGxheTogXCJmbGV4XCIsIGp1c3RpZnlDb250ZW50OiBcInNwYWNlLWJldHdlZW5cIiwgYWxpZ25JdGVtczogXCJjZW50ZXJcIiB9fT5cblx0XHRcdDxzcGFuIHN0eWxlPSR7eyBtYXJnaW5Cb3R0b206IFwiNXB4XCIsIG1heFdpZHRoOiBcIjI1MHB4XCIsIC4uLlRSVU5DQVRFIH19PiR7ZmllbGQubmFtZX08L3NwYW4+XG5cdFx0XHQke3NvcnRCdXR0b259XG5cdFx0PC9kaXY+XG5cdFx0JHt2ZXJ0aWNhbFJlc2l6ZUhhbmRsZX1cblx0XHQ8c3BhbiBjbGFzcz1cImdyYXlcIiBzdHlsZT0ke3sgZm9udFdlaWdodDogNDAwLCBmb250U2l6ZTogXCIxMnB4XCIsIHVzZXJTZWxlY3Q6IFwibm9uZVwiIH19PiR7Zm9ybWF0RGF0YVR5cGUoZmllbGQudHlwZSl9PC9zcGFuPlxuXHRcdCR7dmlzPy5wbG90Py5ub2RlKCl9XG5cdDwvdGg+YDtcblxuXHRzaWduYWxzLmVmZmVjdCgoKSA9PiB7XG5cdFx0dXBhcnJvdy5zZXRBdHRyaWJ1dGUoXCJzdHJva2VcIiwgXCJ2YXIoLS1tb29uLWdyYXkpXCIpO1xuXHRcdGRvd25hcnJvdy5zZXRBdHRyaWJ1dGUoXCJzdHJva2VcIiwgXCJ2YXIoLS1tb29uLWdyYXkpXCIpO1xuXHRcdC8vIEBkZW5vLWZtdC1pZ25vcmVcblx0XHRsZXQgZWxlbWVudCA9IHsgXCJhc2NcIjogdXBhcnJvdywgXCJkZXNjXCI6IGRvd25hcnJvdywgXCJ1bnNldFwiOiBudWxsIH1bc29ydFN0YXRlLnZhbHVlXTtcblx0XHRlbGVtZW50Py5zZXRBdHRyaWJ1dGUoXCJzdHJva2VcIiwgXCJ2YXIoLS1kYXJrLWdyYXkpXCIpO1xuXHR9KTtcblxuXHRzaWduYWxzLmVmZmVjdCgoKSA9PiB7XG5cdFx0c29ydEJ1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gYnV0dG9uVmlzaWJsZS52YWx1ZSA/IFwidmlzaWJsZVwiIDogXCJoaWRkZW5cIjtcblx0fSk7XG5cblx0c2lnbmFscy5lZmZlY3QoKCkgPT4ge1xuXHRcdHRoLnN0eWxlLndpZHRoID0gYCR7d2lkdGgudmFsdWV9cHhgO1xuXHR9KTtcblxuXHR0aC5hZGRFdmVudExpc3RlbmVyKFwibW91c2VvdmVyXCIsICgpID0+IHtcblx0XHRpZiAoc29ydFN0YXRlLnZhbHVlID09PSBcInVuc2V0XCIpIGJ1dHRvblZpc2libGUudmFsdWUgPSB0cnVlO1xuXHR9KTtcblxuXHR0aC5hZGRFdmVudExpc3RlbmVyKFwibW91c2VsZWF2ZVwiLCAoKSA9PiB7XG5cdFx0aWYgKHNvcnRTdGF0ZS52YWx1ZSA9PT0gXCJ1bnNldFwiKSBidXR0b25WaXNpYmxlLnZhbHVlID0gZmFsc2U7XG5cdH0pO1xuXG5cdHRoLmFkZEV2ZW50TGlzdGVuZXIoXCJkYmxjbGlja1wiLCAoZXZlbnQpID0+IHtcblx0XHQvLyByZXNldCBjb2x1bW4gd2lkdGggYnV0IHdlIGRvbid0IHdhbnQgdG8gaW50ZXJmZXJlIHdpdGggc29tZW9uZVxuXHRcdC8vIGRvdWJsZS1jbGlja2luZyB0aGUgc29ydCBidXR0b25cblx0XHQvLyBpZiB0aGUgbW91c2UgaXMgd2l0aGluIHRoZSBzb3J0IGJ1dHRvbiwgZG9uJ3QgcmVzZXQgdGhlIHdpZHRoXG5cdFx0aWYgKFxuXHRcdFx0ZXZlbnQub2Zmc2V0WCA8IHNvcnRCdXR0b24ub2Zmc2V0V2lkdGggJiZcblx0XHRcdGV2ZW50Lm9mZnNldFkgPCBzb3J0QnV0dG9uLm9mZnNldEhlaWdodFxuXHRcdCkge1xuXHRcdFx0cmV0dXJuO1xuXHRcdH1cblx0XHR3aWR0aC52YWx1ZSA9IG1pbldpZHRoO1xuXHR9KTtcblxuXHR2ZXJ0aWNhbFJlc2l6ZUhhbmRsZS5hZGRFdmVudExpc3RlbmVyKFwibW91c2Vkb3duXCIsIChldmVudCkgPT4ge1xuXHRcdGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cdFx0bGV0IHN0YXJ0WCA9IGV2ZW50LmNsaWVudFg7XG5cdFx0bGV0IHN0YXJ0V2lkdGggPSB0aC5vZmZzZXRXaWR0aCAtXG5cdFx0XHRwYXJzZUZsb2F0KGdldENvbXB1dGVkU3R5bGUodGgpLnBhZGRpbmdMZWZ0KSAtXG5cdFx0XHRwYXJzZUZsb2F0KGdldENvbXB1dGVkU3R5bGUodGgpLnBhZGRpbmdSaWdodCk7XG5cdFx0ZnVuY3Rpb24gb25Nb3VzZU1vdmUoLyoqIEB0eXBlIHtNb3VzZUV2ZW50fSAqLyBldmVudDogTW91c2VFdmVudCkge1xuXHRcdFx0bGV0IGR4ID0gZXZlbnQuY2xpZW50WCAtIHN0YXJ0WDtcblx0XHRcdHdpZHRoLnZhbHVlID0gTWF0aC5tYXgobWluV2lkdGgsIHN0YXJ0V2lkdGggKyBkeCk7XG5cdFx0XHR2ZXJ0aWNhbFJlc2l6ZUhhbmRsZS5zdHlsZS5iYWNrZ3JvdW5kQ29sb3IgPSBcInZhcigtLWxpZ2h0LXNpbHZlcilcIjtcblx0XHR9XG5cdFx0ZnVuY3Rpb24gb25Nb3VzZVVwKCkge1xuXHRcdFx0dmVydGljYWxSZXNpemVIYW5kbGUuc3R5bGUuYmFja2dyb3VuZENvbG9yID0gXCJ0cmFuc3BhcmVudFwiO1xuXHRcdFx0ZG9jdW1lbnQucmVtb3ZlRXZlbnRMaXN0ZW5lcihcIm1vdXNlbW92ZVwiLCBvbk1vdXNlTW92ZSk7XG5cdFx0XHRkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKFwibW91c2V1cFwiLCBvbk1vdXNlVXApO1xuXHRcdH1cblx0XHRkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKFwibW91c2Vtb3ZlXCIsIG9uTW91c2VNb3ZlKTtcblx0XHRkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKFwibW91c2V1cFwiLCBvbk1vdXNlVXApO1xuXHR9KTtcblxuXHR2ZXJ0aWNhbFJlc2l6ZUhhbmRsZS5hZGRFdmVudExpc3RlbmVyKFwibW91c2VvdmVyXCIsICgpID0+IHtcblx0XHR2ZXJ0aWNhbFJlc2l6ZUhhbmRsZS5zdHlsZS5iYWNrZ3JvdW5kQ29sb3IgPSBcInZhcigtLWxpZ2h0LXNpbHZlcilcIjtcblx0fSk7XG5cblx0dmVydGljYWxSZXNpemVIYW5kbGUuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlbGVhdmVcIiwgKCkgPT4ge1xuXHRcdHZlcnRpY2FsUmVzaXplSGFuZGxlLnN0eWxlLmJhY2tncm91bmRDb2xvciA9IFwidHJhbnNwYXJlbnRcIjtcblx0fSk7XG5cblx0cmV0dXJuIE9iamVjdC5hc3NpZ24odGgsIHsgdmlzLCBzb3J0U3RhdGUgfSk7XG59XG5cbi8qKlxuICogUmV0dXJuIGEgZm9ybWF0dGVyIGZvciBlYWNoIGZpZWxkIGluIHRoZSBzY2hlbWFcbiAqL1xuZnVuY3Rpb24gZm9ybWF0b2Yoc2NoZW1hOiBhcnJvdy5TY2hlbWEpIHtcblx0Y29uc3QgZm9ybWF0OiBSZWNvcmQ8c3RyaW5nLCAodmFsdWU6IHVua25vd24pID0+IHN0cmluZz4gPSBPYmplY3QuY3JlYXRlKFxuXHRcdG51bGwsXG5cdCk7XG5cdGZvciAoY29uc3QgZmllbGQgb2Ygc2NoZW1hLmZpZWxkcykge1xuXHRcdGZvcm1hdFtmaWVsZC5uYW1lXSA9IGZvcm1hdHRlckZvclZhbHVlKGZpZWxkLnR5cGUpO1xuXHR9XG5cdHJldHVybiBmb3JtYXQ7XG59XG5cbi8qKlxuICogUmV0dXJuIGEgY2xhc3MgdHlwZSBvZiBlYWNoIGZpZWxkIGluIHRoZSBzY2hlbWEuXG4gKi9cbmZ1bmN0aW9uIGNsYXNzb2Yoc2NoZW1hOiBhcnJvdy5TY2hlbWEpOiBSZWNvcmQ8c3RyaW5nLCBcIm51bWJlclwiIHwgXCJkYXRlXCI+IHtcblx0Y29uc3QgY2xhc3NlczogUmVjb3JkPHN0cmluZywgXCJudW1iZXJcIiB8IFwiZGF0ZVwiPiA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG5cdGZvciAoY29uc3QgZmllbGQgb2Ygc2NoZW1hLmZpZWxkcykge1xuXHRcdGlmIChcblx0XHRcdGFycm93LkRhdGFUeXBlLmlzSW50KGZpZWxkLnR5cGUpIHx8XG5cdFx0XHRhcnJvdy5EYXRhVHlwZS5pc0Zsb2F0KGZpZWxkLnR5cGUpXG5cdFx0KSB7XG5cdFx0XHRjbGFzc2VzW2ZpZWxkLm5hbWVdID0gXCJudW1iZXJcIjtcblx0XHR9XG5cdFx0aWYgKFxuXHRcdFx0YXJyb3cuRGF0YVR5cGUuaXNEYXRlKGZpZWxkLnR5cGUpIHx8XG5cdFx0XHRhcnJvdy5EYXRhVHlwZS5pc1RpbWVzdGFtcChmaWVsZC50eXBlKVxuXHRcdCkge1xuXHRcdFx0Y2xhc3Nlc1tmaWVsZC5uYW1lXSA9IFwiZGF0ZVwiO1xuXHRcdH1cblx0fVxuXHRyZXR1cm4gY2xhc3Nlcztcbn1cblxuZnVuY3Rpb24gaGlnaGxpZ2h0KGNlbGw6IEhUTUxUYWJsZUNlbGxFbGVtZW50LCByb3c6IEhUTUxUYWJsZVJvd0VsZW1lbnQpIHtcblx0aWYgKHJvdy5maXJzdENoaWxkICE9PSBjZWxsICYmIGNlbGwgIT09IHJvdy5sYXN0RWxlbWVudENoaWxkKSB7XG5cdFx0Y2VsbC5zdHlsZS5ib3JkZXIgPSBcIjFweCBzb2xpZCB2YXIoLS1tb29uLWdyYXkpXCI7XG5cdH1cblx0cm93LnN0eWxlLmJhY2tncm91bmRDb2xvciA9IFwidmFyKC0tbGlnaHQtc2lsdmVyKVwiO1xufVxuXG5mdW5jdGlvbiByZW1vdmVIaWdobGlnaHQoY2VsbDogSFRNTFRhYmxlQ2VsbEVsZW1lbnQsIHJvdzogSFRNTFRhYmxlUm93RWxlbWVudCkge1xuXHRjZWxsLnN0eWxlLnJlbW92ZVByb3BlcnR5KFwiYm9yZGVyXCIpO1xuXHRyb3cuc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJiYWNrZ3JvdW5kLWNvbG9yXCIpO1xufVxuXG5mdW5jdGlvbiBpc1RhYmxlQ2VsbEVsZW1lbnQobm9kZTogdW5rbm93bik6IG5vZGUgaXMgSFRNTFRhYmxlRGF0YUNlbGxFbGVtZW50IHtcblx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIHRhZ05hbWUgaXMgbm90IGRlZmluZWQgb24gdW5rbm93blxuXHRyZXR1cm4gbm9kZT8udGFnTmFtZSA9PT0gXCJURFwiO1xufVxuXG5mdW5jdGlvbiBpc1RhYmxlUm93RWxlbWVudChub2RlOiB1bmtub3duKTogbm9kZSBpcyBIVE1MVGFibGVSb3dFbGVtZW50IHtcblx0cmV0dXJuIG5vZGUgaW5zdGFuY2VvZiBIVE1MVGFibGVSb3dFbGVtZW50O1xufVxuXG4vKiogQHBhcmFtIHtzdHJpbmd9IHZhbHVlICovXG5mdW5jdGlvbiBzaG91bGRHcmF5b3V0VmFsdWUodmFsdWU6IHN0cmluZykge1xuXHRyZXR1cm4gKFxuXHRcdHZhbHVlID09PSBcIm51bGxcIiB8fFxuXHRcdHZhbHVlID09PSBcInVuZGVmaW5lZFwiIHx8XG5cdFx0dmFsdWUgPT09IFwiTmFOXCIgfHxcblx0XHR2YWx1ZSA9PT0gXCJUT0RPXCJcblx0KTtcbn1cblxuZnVuY3Rpb24gaXNUYWJsZUNvbHVtbkhlYWRlcldpdGhTdmcoXG5cdG5vZGU6IHVua25vd24sXG4pOiBub2RlIGlzIFJldHVyblR5cGU8dHlwZW9mIHRoY29sPiB7XG5cdHJldHVybiBub2RlIGluc3RhbmNlb2YgSFRNTFRhYmxlQ2VsbEVsZW1lbnQgJiYgXCJ2aXNcIiBpbiBub2RlO1xufVxuXG4vKipcbiAqIEEgbW9zYWljIFNRTCBleHByZXNzaW9uIGZvciBhc2NlbmRpbmcgb3JkZXJcbiAqXG4gKiBUaGUgbm9ybWFsIGJlaGF2aW9yIGluIFNRTCBpcyB0byBzb3J0IG51bGxzIGZpcnN0IHdoZW4gc29ydGluZyBpbiBhc2NlbmRpbmcgb3JkZXIuXG4gKiBUaGlzIGZ1bmN0aW9uIHJldHVybnMgYW4gZXhwcmVzc2lvbiB0aGF0IHNvcnRzIG51bGxzIGxhc3QgKGkuZS4sIGBOVUxMUyBMQVNUYCksXG4gKiBsaWtlIHRoZSBgZGVzY2AgZnVuY3Rpb24uXG4gKlxuICogQHBhcmFtIGZpZWxkXG4gKi9cbmZ1bmN0aW9uIGFzYyhmaWVsZDogc3RyaW5nKTogU1FMRXhwcmVzc2lvbiB7XG5cdC8vIGRvZXNuJ3Qgc29ydCBudWxscyBmb3IgYXNjXG5cdGxldCBleHByID0gZGVzYyhmaWVsZCk7XG5cdC8vIEB0cy1leHBlY3QtZXJyb3IgLSBwcml2YXRlIGZpZWxkXG5cdGV4cHIuX2V4cHJbMF0gPSBleHByLl9leHByWzBdLnJlcGxhY2UoXCJERVNDXCIsIFwiQVNDXCIpO1xuXHRyZXR1cm4gZXhwcjtcbn1cblxuLyoqXG4gKiBBZGRzIGN1c3RvbSB3aGVlbCBiZWhhdmlvciB0byBhbiBIVE1MIGVsZW1lbnQsIGFsbG93aW5nIGVpdGhlciBob3Jpem9udGFsIG9yIHZlcnRpY2FsIHNjcm9sbGluZyBiYXNlZCBvbiB0aGUgc2Nyb2xsIGlucHV0LlxuICogUHJldmVudHMgZGVmYXVsdCBzY3JvbGxpbmcgdG8gc3RvcCBldmVudCBwcm9wYWdhdGlvbiB0byBwYXJlbnQgZWxlbWVudHMuXG4gKlxuICogQHBhcmFtIHtIVE1MRWxlbWVudH0gcm9vdCAtIFRoZSBlbGVtZW50IHRvIGFwcGx5IHRoZSBzY3JvbGwgYmVoYXZpb3IgdG8uXG4gKiBAcGFyYW0ge251bWJlcn0gW3Njcm9sbFRocmVzaG9sZD0xMF0gLSBUaGUgbWluaW11bSBkZWx0YSByZXF1aXJlZCB0byB0cmlnZ2VyIGhvcml6b250YWwgb3IgdmVydGljYWwgc2Nyb2xsaW5nLlxuICovXG5mdW5jdGlvbiBhZGREaXJlY3Rpb25hbFNjcm9sbFdpdGhQcmV2ZW50RGVmYXVsdChcblx0cm9vdDogSFRNTEVsZW1lbnQsXG5cdHNjcm9sbFRocmVzaG9sZDogbnVtYmVyID0gMTAsXG4pIHtcblx0bGV0IGFjY3VtdWxhdGVkRGVsdGFYID0gMDtcblx0bGV0IGFjY3VtdWxhdGVkRGVsdGFZID0gMDtcblxuXHRyb290LmFkZEV2ZW50TGlzdGVuZXIoXG5cdFx0XCJ3aGVlbFwiLFxuXHRcdChldmVudCkgPT4ge1xuXHRcdFx0ZXZlbnQucHJldmVudERlZmF1bHQoKTtcblx0XHRcdGFjY3VtdWxhdGVkRGVsdGFYICs9IGV2ZW50LmRlbHRhWDtcblx0XHRcdGFjY3VtdWxhdGVkRGVsdGFZICs9IGV2ZW50LmRlbHRhWTtcblxuXHRcdFx0aWYgKE1hdGguYWJzKGFjY3VtdWxhdGVkRGVsdGFYKSA+IE1hdGguYWJzKGFjY3VtdWxhdGVkRGVsdGFZKSkge1xuXHRcdFx0XHQvLyBob3Jpem9udGFsIHNjcm9sbGluZ1xuXHRcdFx0XHRpZiAoTWF0aC5hYnMoYWNjdW11bGF0ZWREZWx0YVgpID4gc2Nyb2xsVGhyZXNob2xkKSB7XG5cdFx0XHRcdFx0cm9vdC5zY3JvbGxMZWZ0ICs9IGFjY3VtdWxhdGVkRGVsdGFYO1xuXHRcdFx0XHRcdGFjY3VtdWxhdGVkRGVsdGFYID0gMDtcblx0XHRcdFx0XHRhY2N1bXVsYXRlZERlbHRhWSA9IDA7IC8vIFJlc2V0IFkgdG8gYXZvaWQgdW5pbnRlbnRpb25hbCB2ZXJ0aWNhbCBzY3JvbGxpbmdcblx0XHRcdFx0fVxuXHRcdFx0fSBlbHNlIHtcblx0XHRcdFx0Ly8gdmVydGljYWwgc2Nyb2xsaW5nXG5cdFx0XHRcdGlmIChNYXRoLmFicyhhY2N1bXVsYXRlZERlbHRhWSkgPiBzY3JvbGxUaHJlc2hvbGQpIHtcblx0XHRcdFx0XHRyb290LnNjcm9sbFRvcCArPSBhY2N1bXVsYXRlZERlbHRhWTtcblx0XHRcdFx0XHRhY2N1bXVsYXRlZERlbHRhWCA9IDA7IC8vIFJlc2V0IFggdG8gYXZvaWQgdW5pbnRlbnRpb25hbCBob3Jpem9udGFsIHNjcm9sbGluZ1xuXHRcdFx0XHRcdGFjY3VtdWxhdGVkRGVsdGFZID0gMDtcblx0XHRcdFx0fVxuXHRcdFx0fVxuXHRcdH0sXG5cdFx0eyBwYXNzaXZlOiBmYWxzZSB9LFxuXHQpO1xufVxuIiwgIi8qKlxuICogRXJyb3IgdGhyb3duIHdoZW4gYW4gYXNzZXJ0aW9uIGZhaWxzLlxuICovXG5leHBvcnQgY2xhc3MgQXNzZXJ0aW9uRXJyb3IgZXh0ZW5kcyBFcnJvciB7XG5cdC8qKiBAcGFyYW0gbWVzc2FnZSBUaGUgZXJyb3IgbWVzc2FnZS4gKi9cblx0Y29uc3RydWN0b3IobWVzc2FnZTogc3RyaW5nKSB7XG5cdFx0c3VwZXIobWVzc2FnZSk7XG5cdFx0dGhpcy5uYW1lID0gXCJBc3NlcnRpb25FcnJvclwiO1xuXHR9XG59XG5cbi8qKlxuICogTWFrZSBhbiBhc3NlcnRpb24uIEFuIGVycm9yIGlzIHRocm93biBpZiBgZXhwcmAgZG9lcyBub3QgaGF2ZSB0cnV0aHkgdmFsdWUuXG4gKlxuICogQHBhcmFtIGV4cHIgVGhlIGV4cHJlc3Npb24gdG8gdGVzdC5cbiAqIEBwYXJhbSBtc2cgVGhlIG1lc3NhZ2UgdG8gZGlzcGxheSBpZiB0aGUgYXNzZXJ0aW9uIGZhaWxzLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYXNzZXJ0KGV4cHI6IHVua25vd24sIG1zZyA9IFwiXCIpOiBhc3NlcnRzIGV4cHIge1xuXHRpZiAoIWV4cHIpIHtcblx0XHR0aHJvdyBuZXcgQXNzZXJ0aW9uRXJyb3IobXNnKTtcblx0fVxufVxuIiwgImltcG9ydCB7IGFzc2VydCB9IGZyb20gXCIuL2Fzc2VydC50c1wiO1xuXG4vKipcbiAqIEFuIGFzeW5jIGl0ZXJhdG9yIHRoYXQgcmVhZHMgZGF0YSBpbiBiYXRjaGVzIGZyb20gYW4gYXN5bmMgc291cmNlLlxuICpcbiAqIEBleGFtcGxlXG4gKiBgYGB0c1xuICogbGV0IGkgPSAwO1xuICogbGV0IGJhdGNoZXMgPSBbWzEsIDIsIDNdLCBbNCwgNSwgNl1dO1xuICogbGV0IHJlcXVlc3ROZXh0QmF0Y2ggPSBhc3luYyAoKSA9PiB7XG4gKiAgIC8vIHNpbXVsYXRlIGZldGNoaW5nIGEgYmF0Y2hcbiAqICAgYXdhaXQgbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHNldFRpbWVvdXQocmVzb2x2ZSwgMTAwMCkpO1xuICogICBsZXQgYmF0Y2ggPSBiYXRjaGVzLnNoaWZ0KCk7XG4gKiAgIHJlYWRlci5lbnF1ZXVlQmF0Y2goYmF0Y2gsIHsgbGFzdDogYmF0Y2hlcy5sZW5ndGggPT09IDAgfSk7XG4gKiB9O1xuICogbGV0IHJlYWRlciA9IG5ldyBBc3luY0JhdGNoUmVhZGVyKHJlcXVlc3ROZXh0QmF0Y2gpO1xuICpcbiAqIGZvciBhd2FpdCAobGV0IHsgcm93LCBpbmRleCB9IG9mIHJlYWRlcikge1xuICogICBjb25zb2xlLmxvZyhyb3csIGluZGV4KTtcbiAqIH1cbiAqIGBgYFxuICovXG5leHBvcnQgY2xhc3MgQXN5bmNCYXRjaFJlYWRlcjxUPiB7XG5cdC8qKiB0aGUgaXRlcmFibGUgYmF0Y2hlcyB0byByZWFkICovXG5cdCNiYXRjaGVzOiBBcnJheTx7IGRhdGE6IEl0ZXJhdG9yPFQ+OyBsYXN0OiBib29sZWFuIH0+ID0gW107XG5cdC8qKiB0aGUgaW5kZXggb2YgdGhlIGN1cnJlbnQgcm93ICovXG5cdCNpbmRleDogbnVtYmVyID0gMDtcblx0LyoqIHJlc29sdmVzIGEgcHJvbWlzZSBmb3Igd2hlbiB0aGUgbmV4dCBiYXRjaCBpcyBhdmFpbGFibGUgKi9cblx0I3Jlc29sdmU6ICgoKSA9PiB2b2lkKSB8IG51bGwgPSBudWxsO1xuXHQvKiogdGhlIGN1cnJlbnQgYmF0Y2ggKi9cblx0I2N1cnJlbnQ6IHsgZGF0YTogSXRlcmF0b3I8VD47IGxhc3Q6IGJvb2xlYW4gfSB8IG51bGwgPSBudWxsO1xuXHQvKiogQSBmdW5jdGlvbiB0byByZXF1ZXN0IG1vcmUgZGF0YS4gKi9cblx0I3JlcXVlc3ROZXh0QmF0Y2g6ICgpID0+IHZvaWQ7XG5cdC8qKlxuXHQgKiBAcGFyYW0gcmVxdWVzdE5leHRCYXRjaCAtIGEgZnVuY3Rpb24gdG8gcmVxdWVzdCBtb3JlIGRhdGEuIFdoZW5cblx0ICogdGhpcyBmdW5jdGlvbiBjb21wbGV0ZXMsIGl0IHNob3VsZCBlbnF1ZXVlIHRoZSBuZXh0IGJhdGNoLCBvdGhlcndpc2UgdGhlXG5cdCAqIHJlYWRlciB3aWxsIGJlIHN0dWNrLlxuXHQgKi9cblx0Y29uc3RydWN0b3IocmVxdWVzdE5leHRCYXRjaDogKCkgPT4gdm9pZCkge1xuXHRcdHRoaXMuI3JlcXVlc3ROZXh0QmF0Y2ggPSByZXF1ZXN0TmV4dEJhdGNoO1xuXHR9XG5cdC8qKlxuXHQgKiBFbnF1ZXVlIGEgYmF0Y2ggb2YgZGF0YVxuXHQgKlxuXHQgKiBUaGUgbGFzdCBiYXRjaCBzaG91bGQgaGF2ZSBgbGFzdDogdHJ1ZWAgc2V0LFxuXHQgKiBzbyB0aGUgcmVhZGVyIGNhbiB0ZXJtaW5hdGUgd2hlbiBpdCBoYXNcblx0ICogZXhoYXVzdGVkIGFsbCB0aGUgZGF0YS5cblx0ICpcblx0ICogQHBhcmFtIGJhdGNoIC0gdGhlIGJhdGNoIG9mIGRhdGEgdG8gZW5xdWV1ZVxuXHQgKiBAcGFyYW0gb3B0aW9uc1xuXHQgKiBAcGFyYW0gb3B0aW9ucy5sYXN0IC0gd2hldGhlciB0aGlzIGlzIHRoZSBsYXN0IGJhdGNoXG5cdCAqL1xuXHRlbnF1ZXVlQmF0Y2goYmF0Y2g6IEl0ZXJhdG9yPFQ+LCB7IGxhc3QgfTogeyBsYXN0OiBib29sZWFuIH0pIHtcblx0XHR0aGlzLiNiYXRjaGVzLnB1c2goeyBkYXRhOiBiYXRjaCwgbGFzdCB9KTtcblx0XHRpZiAodGhpcy4jcmVzb2x2ZSkge1xuXHRcdFx0dGhpcy4jcmVzb2x2ZSgpO1xuXHRcdFx0dGhpcy4jcmVzb2x2ZSA9IG51bGw7XG5cdFx0fVxuXHR9XG5cdGFzeW5jIG5leHQoKTogUHJvbWlzZTxJdGVyYXRvclJlc3VsdDx7IHJvdzogVDsgaW5kZXg6IG51bWJlciB9Pj4ge1xuXHRcdGlmICghdGhpcy4jY3VycmVudCkge1xuXHRcdFx0aWYgKHRoaXMuI2JhdGNoZXMubGVuZ3RoID09PSAwKSB7XG5cdFx0XHRcdC8qKiBAdHlwZSB7UHJvbWlzZTx2b2lkPn0gKi9cblx0XHRcdFx0bGV0IHByb21pc2U6IFByb21pc2U8dm9pZD4gPSBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4ge1xuXHRcdFx0XHRcdHRoaXMuI3Jlc29sdmUgPSByZXNvbHZlO1xuXHRcdFx0XHR9KTtcblx0XHRcdFx0dGhpcy4jcmVxdWVzdE5leHRCYXRjaCgpO1xuXHRcdFx0XHRhd2FpdCBwcm9taXNlO1xuXHRcdFx0fVxuXHRcdFx0bGV0IG5leHQgPSB0aGlzLiNiYXRjaGVzLnNoaWZ0KCk7XG5cdFx0XHRhc3NlcnQobmV4dCwgXCJObyBuZXh0IGJhdGNoXCIpO1xuXHRcdFx0dGhpcy4jY3VycmVudCA9IG5leHQ7XG5cdFx0fVxuXHRcdGxldCByZXN1bHQgPSB0aGlzLiNjdXJyZW50LmRhdGEubmV4dCgpO1xuXHRcdGlmIChyZXN1bHQuZG9uZSkge1xuXHRcdFx0aWYgKHRoaXMuI2N1cnJlbnQubGFzdCkge1xuXHRcdFx0XHRyZXR1cm4geyBkb25lOiB0cnVlLCB2YWx1ZTogdW5kZWZpbmVkIH07XG5cdFx0XHR9XG5cdFx0XHR0aGlzLiNjdXJyZW50ID0gbnVsbDtcblx0XHRcdHJldHVybiB0aGlzLm5leHQoKTtcblx0XHR9XG5cdFx0cmV0dXJuIHtcblx0XHRcdGRvbmU6IGZhbHNlLFxuXHRcdFx0dmFsdWU6IHsgcm93OiByZXN1bHQudmFsdWUsIGluZGV4OiB0aGlzLiNpbmRleCsrIH0sXG5cdFx0fTtcblx0fVxufVxuIiwgImltcG9ydCB7IFRlbXBvcmFsIH0gZnJvbSBcIkBqcy10ZW1wb3JhbC9wb2x5ZmlsbFwiO1xuaW1wb3J0ICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuXG4vKipcbiAqIEEgdXRpbGl0eSBmdW5jdGlvbiB0byBjcmVhdGUgYSBmb3JtYXR0ZXIgZm9yIGEgZ2l2ZW4gZGF0YSB0eXBlLlxuICpcbiAqIFRoZSBkYXRhdHlwZSBpcyBvbmx5IHVzZWQgZm9yIHR5cGUgaW5mZXJlbmNlIHRvIGVuc3VyZSB0aGF0IHRoZSBmb3JtYXR0ZXIgaXNcbiAqIGNvcnJlY3RseSB0eXBlZC5cbiAqL1xuZnVuY3Rpb24gZm10PFRWYWx1ZT4oXG5cdF9hcnJvd0RhdGFUeXBlVmFsdWU6IFRWYWx1ZSxcblx0Zm9ybWF0OiAodmFsdWU6IFRWYWx1ZSkgPT4gc3RyaW5nLFxuXHRsb2cgPSBmYWxzZSxcbik6ICh2YWx1ZTogVFZhbHVlIHwgbnVsbCB8IHVuZGVmaW5lZCkgPT4gc3RyaW5nIHtcblx0cmV0dXJuICh2YWx1ZSkgPT4ge1xuXHRcdGlmIChsb2cpIGNvbnNvbGUubG9nKHZhbHVlKTtcblx0XHRpZiAodmFsdWUgPT09IHVuZGVmaW5lZCB8fCB2YWx1ZSA9PT0gbnVsbCkge1xuXHRcdFx0cmV0dXJuIHN0cmluZ2lmeSh2YWx1ZSk7XG5cdFx0fVxuXHRcdHJldHVybiBmb3JtYXQodmFsdWUpO1xuXHR9O1xufVxuXG5mdW5jdGlvbiBzdHJpbmdpZnkoeDogdW5rbm93bik6IHN0cmluZyB7XG5cdHJldHVybiBgJHt4fWA7XG59XG5cbi8qKiBAcGFyYW0ge2Fycm93LkRhdGFUeXBlfSB0eXBlICovXG5leHBvcnQgZnVuY3Rpb24gZm9ybWF0RGF0YVR5cGUodHlwZTogYXJyb3cuRGF0YVR5cGUpIHtcblx0Ly8gc3BlY2lhbCBjYXNlIHNvbWUgdHlwZXNcblx0aWYgKGFycm93LkRhdGFUeXBlLmlzTGFyZ2VCaW5hcnkodHlwZSkpIHJldHVybiBcImxhcmdlIGJpbmFyeVwiO1xuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNMYXJnZVV0ZjgodHlwZSkpIHJldHVybiBcImxhcmdlIHV0ZjhcIjtcblx0Ly8gb3RoZXJ3aXNlLCBqdXN0IHN0cmluZ2lmeSBhbmQgbG93ZXJjYXNlXG5cdHJldHVybiB0eXBlXG5cdFx0LnRvU3RyaW5nKClcblx0XHQudG9Mb3dlckNhc2UoKVxuXHRcdC5yZXBsYWNlKFwiPHNlY29uZD5cIiwgXCJbc11cIilcblx0XHQucmVwbGFjZShcIjxtaWxsaXNlY29uZD5cIiwgXCJbbXNdXCIpXG5cdFx0LnJlcGxhY2UoXCI8bWljcm9zZWNvbmQ+XCIsIFwiW1x1MDBCNXNdXCIpXG5cdFx0LnJlcGxhY2UoXCI8bmFub3NlY29uZD5cIiwgXCJbbnNdXCIpXG5cdFx0LnJlcGxhY2UoXCI8ZGF5PlwiLCBcIltkYXldXCIpXG5cdFx0LnJlcGxhY2UoXCJkaWN0aW9uYXJ5PFwiLCBcImRpY3Q8XCIpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7YXJyb3cuRGF0YVR5cGV9IHR5cGVcbiAqIEByZXR1cm5zIHsodmFsdWU6IGFueSkgPT4gc3RyaW5nfVxuICovXG5leHBvcnQgZnVuY3Rpb24gZm9ybWF0dGVyRm9yVmFsdWUoXG5cdHR5cGU6IGFycm93LkRhdGFUeXBlLFxuXHQvLyBkZW5vLWxpbnQtaWdub3JlIG5vLWV4cGxpY2l0LWFueVxuKTogKHZhbHVlOiBhbnkpID0+IHN0cmluZyB7XG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc051bGwodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCBzdHJpbmdpZnkpO1xuXHR9XG5cblx0aWYgKFxuXHRcdGFycm93LkRhdGFUeXBlLmlzSW50KHR5cGUpIHx8XG5cdFx0YXJyb3cuRGF0YVR5cGUuaXNGbG9hdCh0eXBlKVxuXHQpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAodmFsdWUpID0+IHtcblx0XHRcdGlmIChOdW1iZXIuaXNOYU4odmFsdWUpKSByZXR1cm4gXCJOYU5cIjtcblx0XHRcdHJldHVybiB2YWx1ZSA9PT0gMCA/IFwiMFwiIDogdmFsdWUudG9Mb2NhbGVTdHJpbmcoXCJlblwiKTsgLy8gaGFuZGxlIG5lZ2F0aXZlIHplcm9cblx0XHR9KTtcblx0fVxuXG5cdGlmIChcblx0XHRhcnJvdy5EYXRhVHlwZS5pc0JpbmFyeSh0eXBlKSB8fFxuXHRcdGFycm93LkRhdGFUeXBlLmlzRml4ZWRTaXplQmluYXJ5KHR5cGUpIHx8XG5cdFx0YXJyb3cuRGF0YVR5cGUuaXNMYXJnZUJpbmFyeSh0eXBlKVxuXHQpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAoYnl0ZXMpID0+IHtcblx0XHRcdGxldCBtYXhsZW4gPSAzMjtcblx0XHRcdGxldCByZXN1bHQgPSBcImInXCI7XG5cdFx0XHRmb3IgKGxldCBpID0gMDsgaSA8IE1hdGgubWluKGJ5dGVzLmxlbmd0aCwgbWF4bGVuKTsgaSsrKSB7XG5cdFx0XHRcdGNvbnN0IGJ5dGUgPSBieXRlc1tpXTtcblx0XHRcdFx0aWYgKGJ5dGUgPj0gMzIgJiYgYnl0ZSA8PSAxMjYpIHtcblx0XHRcdFx0XHQvLyBBU0NJSSBwcmludGFibGUgY2hhcmFjdGVycyByYW5nZSBmcm9tIDMyIChzcGFjZSkgdG8gMTI2ICh+KVxuXHRcdFx0XHRcdHJlc3VsdCArPSBTdHJpbmcuZnJvbUNoYXJDb2RlKGJ5dGUpO1xuXHRcdFx0XHR9IGVsc2Uge1xuXHRcdFx0XHRcdHJlc3VsdCArPSBcIlxcXFx4XCIgKyAoXCIwMFwiICsgYnl0ZS50b1N0cmluZygxNikpLnNsaWNlKC0yKTtcblx0XHRcdFx0fVxuXHRcdFx0fVxuXHRcdFx0aWYgKGJ5dGVzLmxlbmd0aCA+IG1heGxlbikgcmVzdWx0ICs9IFwiLi4uXCI7XG5cdFx0XHRyZXN1bHQgKz0gXCInXCI7XG5cdFx0XHRyZXR1cm4gcmVzdWx0O1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzVXRmOCh0eXBlKSB8fCBhcnJvdy5EYXRhVHlwZS5pc0xhcmdlVXRmOCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsICh0ZXh0KSA9PiB0ZXh0KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0Jvb2wodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCBzdHJpbmdpZnkpO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzRGVjaW1hbCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsICgpID0+IFwiVE9ET1wiKTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0RhdGUodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAobXMpID0+IHtcblx0XHRcdC8vIEFsd2F5cyByZXR1cm5zIHZhbHVlIGluIG1pbGxpc2Vjb25kc1xuXHRcdFx0Ly8gaHR0cHM6Ly9naXRodWIuY29tL2FwYWNoZS9hcnJvdy9ibG9iLzg5ZDYzNTQwNjhjMTFhNjZmY2VjMmYzNGQwNDE0ZGFjYTMyN2UyZTAvanMvc3JjL3Zpc2l0b3IvZ2V0LnRzI0wxNjctTDE3MVxuXHRcdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnRcblx0XHRcdFx0LmZyb21FcG9jaE1pbGxpc2Vjb25kcyhtcylcblx0XHRcdFx0LnRvWm9uZWREYXRlVGltZUlTTyhcIlVUQ1wiKVxuXHRcdFx0XHQudG9QbGFpbkRhdGUoKVxuXHRcdFx0XHQudG9TdHJpbmcoKTtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc1RpbWUodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAobXMpID0+IHtcblx0XHRcdHJldHVybiBpbnN0YW50RnJvbVRpbWVVbml0KG1zLCB0eXBlLnVuaXQpXG5cdFx0XHRcdC50b1pvbmVkRGF0ZVRpbWVJU08oXCJVVENcIilcblx0XHRcdFx0LnRvUGxhaW5UaW1lKClcblx0XHRcdFx0LnRvU3RyaW5nKCk7XG5cdFx0fSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNUaW1lc3RhbXAodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAobXMpID0+IHtcblx0XHRcdC8vIEFsd2F5cyByZXR1cm5zIHZhbHVlIGluIG1pbGxpc2Vjb25kc1xuXHRcdFx0Ly8gaHR0cHM6Ly9naXRodWIuY29tL2FwYWNoZS9hcnJvdy9ibG9iLzg5ZDYzNTQwNjhjMTFhNjZmY2VjMmYzNGQwNDE0ZGFjYTMyN2UyZTAvanMvc3JjL3Zpc2l0b3IvZ2V0LnRzI0wxNzMtTDE5MFxuXHRcdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnRcblx0XHRcdFx0LmZyb21FcG9jaE1pbGxpc2Vjb25kcyhtcylcblx0XHRcdFx0LnRvWm9uZWREYXRlVGltZUlTTyhcIlVUQ1wiKVxuXHRcdFx0XHQudG9QbGFpbkRhdGVUaW1lKClcblx0XHRcdFx0LnRvU3RyaW5nKCk7XG5cdFx0fSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNJbnRlcnZhbCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChfdmFsdWUpID0+IHtcblx0XHRcdHJldHVybiBcIlRPRE9cIjtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0R1cmF0aW9uKHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKGJpZ2ludFZhbHVlKSA9PiB7XG5cdFx0XHQvLyBodHRwczovL3RjMzkuZXMvcHJvcG9zYWwtdGVtcG9yYWwvZG9jcy9kdXJhdGlvbi5odG1sI3RvU3RyaW5nXG5cdFx0XHRyZXR1cm4gZHVyYXRpb25Gcm9tVGltZVVuaXQoYmlnaW50VmFsdWUsIHR5cGUudW5pdCkudG9TdHJpbmcoKTtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0xpc3QodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAodmFsdWUpID0+IHtcblx0XHRcdC8vIFRPRE86IFNvbWUgcmVjdXJzaXZlIGZvcm1hdHRpbmc/XG5cdFx0XHRyZXR1cm4gdmFsdWUudG9TdHJpbmcoKTtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc1N0cnVjdCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsICh2YWx1ZSkgPT4ge1xuXHRcdFx0Ly8gVE9ETzogU29tZSByZWN1cnNpdmUgZm9ybWF0dGluZz9cblx0XHRcdHJldHVybiB2YWx1ZS50b1N0cmluZygpO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzVW5pb24odHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAoX3ZhbHVlKSA9PiB7XG5cdFx0XHRyZXR1cm4gXCJUT0RPXCI7XG5cdFx0fSk7XG5cdH1cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzTWFwKHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKF92YWx1ZSkgPT4ge1xuXHRcdFx0cmV0dXJuIFwiVE9ET1wiO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzRGljdGlvbmFyeSh0eXBlKSkge1xuXHRcdGxldCBmb3JtYXR0ZXIgPSBmb3JtYXR0ZXJGb3JWYWx1ZSh0eXBlLmRpY3Rpb25hcnkpO1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIGZvcm1hdHRlcik7XG5cdH1cblxuXHRyZXR1cm4gKCkgPT4gYFVuc3VwcG9ydGVkIHR5cGU6ICR7dHlwZX1gO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7bnVtYmVyIHwgYmlnaW50fSB2YWx1ZVxuICogQHBhcmFtIHthcnJvdy5UaW1lVW5pdH0gdW5pdFxuICovXG5mdW5jdGlvbiBpbnN0YW50RnJvbVRpbWVVbml0KHZhbHVlOiBudW1iZXIgfCBiaWdpbnQsIHVuaXQ6IGFycm93LlRpbWVVbml0KSB7XG5cdGlmICh1bml0ID09PSBhcnJvdy5UaW1lVW5pdC5TRUNPTkQpIHtcblx0XHRpZiAodHlwZW9mIHZhbHVlID09PSBcImJpZ2ludFwiKSB2YWx1ZSA9IE51bWJlcih2YWx1ZSk7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnQuZnJvbUVwb2NoU2Vjb25kcyh2YWx1ZSk7XG5cdH1cblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0Lk1JTExJU0VDT05EKSB7XG5cdFx0aWYgKHR5cGVvZiB2YWx1ZSA9PT0gXCJiaWdpbnRcIikgdmFsdWUgPSBOdW1iZXIodmFsdWUpO1xuXHRcdHJldHVybiBUZW1wb3JhbC5JbnN0YW50LmZyb21FcG9jaE1pbGxpc2Vjb25kcyh2YWx1ZSk7XG5cdH1cblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0Lk1JQ1JPU0VDT05EKSB7XG5cdFx0aWYgKHR5cGVvZiB2YWx1ZSA9PT0gXCJudW1iZXJcIikgdmFsdWUgPSBCaWdJbnQodmFsdWUpO1xuXHRcdHJldHVybiBUZW1wb3JhbC5JbnN0YW50LmZyb21FcG9jaE1pY3Jvc2Vjb25kcyh2YWx1ZSk7XG5cdH1cblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0Lk5BTk9TRUNPTkQpIHtcblx0XHRpZiAodHlwZW9mIHZhbHVlID09PSBcIm51bWJlclwiKSB2YWx1ZSA9IEJpZ0ludCh2YWx1ZSk7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnQuZnJvbUVwb2NoTmFub3NlY29uZHModmFsdWUpO1xuXHR9XG5cdHRocm93IG5ldyBFcnJvcihcIkludmFsaWQgVGltZVVuaXRcIik7XG59XG5cbi8qKlxuICogQHBhcmFtIHtudW1iZXIgfCBiaWdpbnR9IHZhbHVlXG4gKiBAcGFyYW0ge2Fycm93LlRpbWVVbml0fSB1bml0XG4gKi9cbmZ1bmN0aW9uIGR1cmF0aW9uRnJvbVRpbWVVbml0KHZhbHVlOiBudW1iZXIgfCBiaWdpbnQsIHVuaXQ6IGFycm93LlRpbWVVbml0KSB7XG5cdC8vIFRPRE86IFRlbXBvcmFsLkR1cmF0aW9uIHBvbHlmaWxsIG9ubHkgc3VwcG9ydHMgbnVtYmVyIG5vdCBiaWdpbnRcblx0dmFsdWUgPSBOdW1iZXIodmFsdWUpO1xuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuU0VDT05EKSB7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkR1cmF0aW9uLmZyb20oeyBzZWNvbmRzOiB2YWx1ZSB9KTtcblx0fVxuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuTUlMTElTRUNPTkQpIHtcblx0XHRyZXR1cm4gVGVtcG9yYWwuRHVyYXRpb24uZnJvbSh7IG1pbGxpc2Vjb25kczogdmFsdWUgfSk7XG5cdH1cblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0Lk1JQ1JPU0VDT05EKSB7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkR1cmF0aW9uLmZyb20oeyBtaWNyb3NlY29uZHM6IHZhbHVlIH0pO1xuXHR9XG5cdGlmICh1bml0ID09PSBhcnJvdy5UaW1lVW5pdC5OQU5PU0VDT05EKSB7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkR1cmF0aW9uLmZyb20oeyBuYW5vc2Vjb25kczogdmFsdWUgfSk7XG5cdH1cblx0dGhyb3cgbmV3IEVycm9yKFwiSW52YWxpZCBUaW1lVW5pdFwiKTtcbn1cbiIsICIvLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLWNvcmUuZC50c1wiO1xuaW1wb3J0IHtcblx0dHlwZSBDb2x1bW5GaWVsZCxcblx0dHlwZSBGaWVsZEluZm8sXG5cdHR5cGUgRmllbGRSZXF1ZXN0LFxuXHRNb3NhaWNDbGllbnQsXG5cdHR5cGUgU2VsZWN0aW9uLFxufSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtY29yZVwiO1xuLy8gQGRlbm8tdHlwZXM9XCIuLi9kZXBzL21vc2FpYy1zcWwuZC50c1wiO1xuaW1wb3J0IHsgY291bnQsIFF1ZXJ5LCBTUUxFeHByZXNzaW9uIH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuaW1wb3J0ICogYXMgbXBsb3QgZnJvbSBcIkB1d2RhdGEvbW9zYWljLXBsb3RcIjtcbmltcG9ydCB0eXBlICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuXG5pbXBvcnQgeyBDcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QgfSBmcm9tIFwiLi4vdXRpbHMvQ3Jvc3NmaWx0ZXJIaXN0b2dyYW1QbG90LnRzXCI7XG5cbmltcG9ydCB0eXBlIHsgTWFyayB9IGZyb20gXCIuLi90eXBlcy50c1wiO1xuaW1wb3J0IHsgYXNzZXJ0IH0gZnJvbSBcIi4uL3V0aWxzL2Fzc2VydC50c1wiO1xuXG4vKiogQW4gb3B0aW9ucyBiYWcgZm9yIHRoZSBIaXN0b2dyYW0gTW9zaWFjIGNsaWVudC4gKi9cbmludGVyZmFjZSBIaXN0b2dyYW1PcHRpb25zIHtcblx0LyoqIFRoZSB0YWJsZSB0byBxdWVyeS4gKi9cblx0dGFibGU6IHN0cmluZztcblx0LyoqIFRoZSBjb2x1bW4gdG8gdXNlIGZvciB0aGUgaGlzdG9ncmFtLiAqL1xuXHRjb2x1bW46IHN0cmluZztcblx0LyoqIFRoZSB0eXBlIG9mIHRoZSBjb2x1bW4uIE11c3QgYmUgXCJudW1iZXJcIiBvciBcImRhdGVcIi4gKi9cblx0dHlwZTogXCJudW1iZXJcIiB8IFwiZGF0ZVwiO1xuXHQvKiogQSBtb3NhaWMgc2VsZWN0aW9uIHRvIGZpbHRlciB0aGUgZGF0YS4gKi9cblx0ZmlsdGVyQnk6IFNlbGVjdGlvbjtcbn1cblxudHlwZSBCaW5UYWJsZSA9IGFycm93LlRhYmxlPHsgeDE6IGFycm93LkludDsgeDI6IGFycm93LkludDsgeTogYXJyb3cuSW50IH0+O1xuXG4vKiogUmVwcmVzZW50cyBhIENyb3NzLWZpbHRlcmVkIEhpc3RvZ3JhbSAqL1xuZXhwb3J0IGNsYXNzIEhpc3RvZ3JhbSBleHRlbmRzIE1vc2FpY0NsaWVudCBpbXBsZW1lbnRzIE1hcmsge1xuXHQjc291cmNlOiB7IHRhYmxlOiBzdHJpbmc7IGNvbHVtbjogc3RyaW5nOyB0eXBlOiBcIm51bWJlclwiIHwgXCJkYXRlXCIgfTtcblx0I2VsOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdCNzZWxlY3Q6IHtcblx0XHR4MTogQ29sdW1uRmllbGQ7XG5cdFx0eDI6IENvbHVtbkZpZWxkO1xuXHRcdHk6IFNRTEV4cHJlc3Npb247XG5cdH07XG5cdCNpbnRlcnZhbDogbXBsb3QuSW50ZXJ2YWwxRCB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZDtcblx0I2luaXRpYWxpemVkOiBib29sZWFuID0gZmFsc2U7XG5cdCNmaWVsZEluZm86IEZpZWxkSW5mbyB8IHVuZGVmaW5lZDtcblxuXHRzdmc6IFJldHVyblR5cGU8dHlwZW9mIENyb3NzZmlsdGVySGlzdG9ncmFtUGxvdD4gfCB1bmRlZmluZWQ7XG5cblx0Y29uc3RydWN0b3Iob3B0aW9uczogSGlzdG9ncmFtT3B0aW9ucykge1xuXHRcdHN1cGVyKG9wdGlvbnMuZmlsdGVyQnkpO1xuXHRcdHRoaXMuI3NvdXJjZSA9IG9wdGlvbnM7XG5cdFx0Ly8gY2FsbHMgdGhpcy5jaGFubmVsRmllbGQgaW50ZXJuYWxseVxuXHRcdGxldCBiaW4gPSBtcGxvdC5iaW4ob3B0aW9ucy5jb2x1bW4pKHRoaXMsIFwieFwiKTtcblx0XHR0aGlzLiNzZWxlY3QgPSB7IHgxOiBiaW4ueDEsIHgyOiBiaW4ueDIsIHk6IGNvdW50KCkgfTtcblx0XHR0aGlzLiNpbnRlcnZhbCA9IG5ldyBtcGxvdC5JbnRlcnZhbDFEKHRoaXMsIHtcblx0XHRcdGNoYW5uZWw6IFwieFwiLFxuXHRcdFx0c2VsZWN0aW9uOiB0aGlzLmZpbHRlckJ5LFxuXHRcdFx0ZmllbGQ6IHRoaXMuI3NvdXJjZS5jb2x1bW4sXG5cdFx0XHRicnVzaDogdW5kZWZpbmVkLFxuXHRcdH0pO1xuXHR9XG5cblx0ZmllbGRzKCk6IEFycmF5PEZpZWxkUmVxdWVzdD4ge1xuXHRcdHJldHVybiBbXG5cdFx0XHR7XG5cdFx0XHRcdHRhYmxlOiB0aGlzLiNzb3VyY2UudGFibGUsXG5cdFx0XHRcdGNvbHVtbjogdGhpcy4jc291cmNlLmNvbHVtbixcblx0XHRcdFx0c3RhdHM6IFtcIm1pblwiLCBcIm1heFwiXSxcblx0XHRcdH0sXG5cdFx0XTtcblx0fVxuXG5cdGZpZWxkSW5mbyhpbmZvOiBBcnJheTxGaWVsZEluZm8+KSB7XG5cdFx0dGhpcy4jZmllbGRJbmZvID0gaW5mb1swXTtcblx0XHRyZXR1cm4gdGhpcztcblx0fVxuXHQvKipcblx0ICogUmV0dXJuIGEgcXVlcnkgc3BlY2lmeWluZyB0aGUgZGF0YSBuZWVkZWQgYnkgdGhpcyBNYXJrIGNsaWVudC5cblx0ICogQHBhcmFtIGZpbHRlciBUaGUgZmlsdGVyaW5nIGNyaXRlcmlhIHRvIGFwcGx5IGluIHRoZSBxdWVyeS5cblx0ICogQHJldHVybnMgVGhlIGNsaWVudCBxdWVyeVxuXHQgKi9cblx0cXVlcnkoZmlsdGVyOiBBcnJheTxTUUxFeHByZXNzaW9uPiA9IFtdKTogUXVlcnkge1xuXHRcdHJldHVybiBRdWVyeVxuXHRcdFx0LmZyb20oeyBzb3VyY2U6IHRoaXMuI3NvdXJjZS50YWJsZSB9KVxuXHRcdFx0LnNlbGVjdCh0aGlzLiNzZWxlY3QpXG5cdFx0XHQuZ3JvdXBieShbXCJ4MVwiLCBcIngyXCJdKVxuXHRcdFx0LndoZXJlKGZpbHRlcik7XG5cdH1cblxuXHQvKipcblx0ICogUHJvdmlkZSBxdWVyeSByZXN1bHQgZGF0YSB0byB0aGUgbWFyay5cblx0ICovXG5cdHF1ZXJ5UmVzdWx0KGRhdGE6IEJpblRhYmxlKSB7XG5cdFx0bGV0IGJpbnMgPSBBcnJheS5mcm9tKGRhdGEsIChkKSA9PiAoe1xuXHRcdFx0eDA6IGQueDEsXG5cdFx0XHR4MTogZC54Mixcblx0XHRcdGxlbmd0aDogZC55LFxuXHRcdH0pKTtcblx0XHRsZXQgbnVsbENvdW50ID0gMDtcblx0XHRsZXQgbnVsbEJpbkluZGV4ID0gYmlucy5maW5kSW5kZXgoKGIpID0+IGIueDAgPT0gbnVsbCk7XG5cdFx0aWYgKG51bGxCaW5JbmRleCA+PSAwKSB7XG5cdFx0XHRudWxsQ291bnQgPSBiaW5zW251bGxCaW5JbmRleF0ubGVuZ3RoO1xuXHRcdFx0Ymlucy5zcGxpY2UobnVsbEJpbkluZGV4LCAxKTtcblx0XHR9XG5cdFx0aWYgKCF0aGlzLiNpbml0aWFsaXplZCkge1xuXHRcdFx0dGhpcy5zdmcgPSBDcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QoYmlucywge1xuXHRcdFx0XHRudWxsQ291bnQsXG5cdFx0XHRcdHR5cGU6IHRoaXMuI3NvdXJjZS50eXBlLFxuXHRcdFx0fSk7XG5cdFx0XHR0aGlzLiNpbnRlcnZhbD8uaW5pdCh0aGlzLnN2ZywgbnVsbCk7XG5cdFx0XHR0aGlzLiNlbC5hcHBlbmRDaGlsZCh0aGlzLnN2Zyk7XG5cdFx0XHR0aGlzLiNpbml0aWFsaXplZCA9IHRydWU7XG5cdFx0fSBlbHNlIHtcblx0XHRcdHRoaXMuc3ZnPy51cGRhdGUoYmlucywgeyBudWxsQ291bnQgfSk7XG5cdFx0fVxuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cblx0LyogUmVxdWlyZWQgYnkgdGhlIE1hcmsgaW50ZXJmYWNlICovXG5cdHR5cGUgPSBcInJlY3RZXCI7XG5cdC8qKiBSZXF1aXJlZCBieSBgbXBsb3QuYmluYCB0byBnZXQgdGhlIGZpZWxkIGluZm8uICovXG5cdGNoYW5uZWxGaWVsZChjaGFubmVsOiBzdHJpbmcpOiBGaWVsZEluZm8ge1xuXHRcdGFzc2VydChjaGFubmVsID09PSBcInhcIik7XG5cdFx0YXNzZXJ0KHRoaXMuI2ZpZWxkSW5mbywgXCJObyBmaWVsZCBpbmZvIHlldFwiKTtcblx0XHRyZXR1cm4gdGhpcy4jZmllbGRJbmZvO1xuXHR9XG5cdGdldCBwbG90KCkge1xuXHRcdHJldHVybiB7XG5cdFx0XHRub2RlOiAoKSA9PiB0aGlzLiNlbCxcblx0XHRcdGdldEF0dHJpYnV0ZShfbmFtZTogc3RyaW5nKSB7XG5cdFx0XHRcdHJldHVybiB1bmRlZmluZWQ7XG5cdFx0XHR9LFxuXHRcdH07XG5cdH1cbn1cbiIsICJpbXBvcnQgeyBlZmZlY3QsIHNpZ25hbCB9IGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuaW1wb3J0ICogYXMgZDMgZnJvbSBcIi4uL2RlcHMvZDMudHNcIjtcbmltcG9ydCB7IGFzc2VydCB9IGZyb20gXCIuLi91dGlscy9hc3NlcnQudHNcIjtcbmltcG9ydCB7IHRpY2tGb3JtYXR0ZXJGb3JCaW5zIH0gZnJvbSBcIi4vdGljay1mb3JtYXR0ZXItZm9yLWJpbnMudHNcIjtcbmltcG9ydCB0eXBlIHsgQmluLCBTY2FsZSB9IGZyb20gXCIuLi90eXBlcy50c1wiO1xuXG5pbnRlcmZhY2UgSGlzdG9ncmFtT3B0aW9ucyB7XG5cdHR5cGU6IFwibnVtYmVyXCIgfCBcImRhdGVcIjtcblx0d2lkdGg/OiBudW1iZXI7XG5cdGhlaWdodD86IG51bWJlcjtcblx0bWFyZ2luVG9wPzogbnVtYmVyO1xuXHRtYXJnaW5SaWdodD86IG51bWJlcjtcblx0bWFyZ2luQm90dG9tPzogbnVtYmVyO1xuXHRtYXJnaW5MZWZ0PzogbnVtYmVyO1xuXHRudWxsQ291bnQ/OiBudW1iZXI7XG5cdGZpbGxDb2xvcj86IHN0cmluZztcblx0bnVsbEZpbGxDb2xvcj86IHN0cmluZztcblx0YmFja2dyb3VuZEJhckNvbG9yPzogc3RyaW5nO1xufVxuXG4vKipcbiAqIFJldHVybnMgYW4gU1ZHIGVsZW1lbnQuXG4gKlxuICogQHBhcmFtIGJpbnMgLSB0aGUgXCJjb21wbGV0ZVwiLCBvciB0b3RhbCBiaW5zIGZvciB0aGUgY3Jvc3NmaWx0ZXIgaGlzdG9ncmFtLlxuICogQHBhcmFtIG9wdGlvbnMgLSBBIGJhZyBvZiBvcHRpb25zIHRvIGNvbmZpZ3VyZSB0aGUgaGlzdG9ncmFtXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBDcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QoXG5cdGJpbnM6IEFycmF5PEJpbj4sXG5cdHtcblx0XHR0eXBlID0gXCJudW1iZXJcIixcblx0XHR3aWR0aCA9IDEyNSxcblx0XHRoZWlnaHQgPSA0MCxcblx0XHRtYXJnaW5Ub3AgPSAwLFxuXHRcdG1hcmdpblJpZ2h0ID0gMixcblx0XHRtYXJnaW5Cb3R0b20gPSAxMixcblx0XHRtYXJnaW5MZWZ0ID0gMixcblx0XHRudWxsQ291bnQgPSAwLFxuXHRcdGZpbGxDb2xvciA9IFwidmFyKC0tcHJpbWFyeSlcIixcblx0XHRudWxsRmlsbENvbG9yID0gXCJ2YXIoLS1zZWNvbmRhcnkpXCIsXG5cdFx0YmFja2dyb3VuZEJhckNvbG9yID0gXCJ2YXIoLS1tb29uLWdyYXkpXCIsXG5cdH06IEhpc3RvZ3JhbU9wdGlvbnMsXG4pOiBTVkdTVkdFbGVtZW50ICYge1xuXHRzY2FsZTogKHR5cGU6IHN0cmluZykgPT4gU2NhbGU8bnVtYmVyLCBudW1iZXI+O1xuXHR1cGRhdGUoYmluczogQXJyYXk8QmluPiwgb3B0czogeyBudWxsQ291bnQ6IG51bWJlciB9KTogdm9pZDtcbn0ge1xuXHRsZXQgaG92ZXJlZCA9IHNpZ25hbDxudW1iZXIgfCBEYXRlIHwgdW5kZWZpbmVkPih1bmRlZmluZWQpO1xuXHRsZXQgbnVsbEJpbldpZHRoID0gbnVsbENvdW50ID09PSAwID8gMCA6IDU7XG5cdGxldCBzcGFjaW5nID0gbnVsbEJpbldpZHRoID8gNCA6IDA7XG5cdGxldCBleHRlbnQgPSAvKiogQHR5cGUge2NvbnN0fSAqLyAoW1xuXHRcdE1hdGgubWluKC4uLmJpbnMubWFwKChkKSA9PiBkLngwKSksXG5cdFx0TWF0aC5tYXgoLi4uYmlucy5tYXAoKGQpID0+IGQueDEpKSxcblx0XSk7XG5cdGxldCB4ID0gdHlwZSA9PT0gXCJkYXRlXCIgPyBkMy5zY2FsZVV0YygpIDogZDMuc2NhbGVMaW5lYXIoKTtcblx0eFxuXHRcdC5kb21haW4oZXh0ZW50KVxuXHRcdC8vIEB0cy1leHBlY3QtZXJyb3IgLSByYW5nZSBpcyBvayB3aXRoIG51bWJlciBmb3IgYm90aCBudW1iZXIgYW5kIHRpbWVcblx0XHQucmFuZ2UoW21hcmdpbkxlZnQgKyBudWxsQmluV2lkdGggKyBzcGFjaW5nLCB3aWR0aCAtIG1hcmdpblJpZ2h0XSlcblx0XHQubmljZSgpO1xuXG5cdGxldCB5ID0gZDMuc2NhbGVMaW5lYXIoKVxuXHRcdC5kb21haW4oWzAsIE1hdGgubWF4KG51bGxDb3VudCwgLi4uYmlucy5tYXAoKGQpID0+IGQubGVuZ3RoKSldKVxuXHRcdC5yYW5nZShbaGVpZ2h0IC0gbWFyZ2luQm90dG9tLCBtYXJnaW5Ub3BdKTtcblxuXHRsZXQgc3ZnID0gZDMuY3JlYXRlKFwic3ZnXCIpXG5cdFx0LmF0dHIoXCJ3aWR0aFwiLCB3aWR0aClcblx0XHQuYXR0cihcImhlaWdodFwiLCBoZWlnaHQpXG5cdFx0LmF0dHIoXCJ2aWV3Qm94XCIsIFswLCAwLCB3aWR0aCwgaGVpZ2h0XSlcblx0XHQuYXR0cihcInN0eWxlXCIsIFwibWF4LXdpZHRoOiAxMDAlOyBoZWlnaHQ6IGF1dG87IG92ZXJmbG93OiB2aXNpYmxlO1wiKTtcblxuXHR7XG5cdFx0Ly8gYmFja2dyb3VuZCBiYXJzIHdpdGggdGhlIFwidG90YWxcIiBiaW5zXG5cdFx0c3ZnLmFwcGVuZChcImdcIilcblx0XHRcdC5hdHRyKFwiZmlsbFwiLCBiYWNrZ3JvdW5kQmFyQ29sb3IpXG5cdFx0XHQuc2VsZWN0QWxsKFwicmVjdFwiKVxuXHRcdFx0LmRhdGEoYmlucylcblx0XHRcdC5qb2luKFwicmVjdFwiKVxuXHRcdFx0LmF0dHIoXCJ4XCIsIChkKSA9PiB4KGQueDApICsgMS41KVxuXHRcdFx0LmF0dHIoXCJ3aWR0aFwiLCAoZCkgPT4geChkLngxKSAtIHgoZC54MCkgLSAxLjUpXG5cdFx0XHQuYXR0cihcInlcIiwgKGQpID0+IHkoZC5sZW5ndGgpKVxuXHRcdFx0LmF0dHIoXCJoZWlnaHRcIiwgKGQpID0+IHkoMCkgLSB5KGQubGVuZ3RoKSk7XG5cdH1cblxuXHQvLyBGb3JlZ3JvdW5kIGJhcnMgZm9yIHRoZSBjdXJyZW50IHN1YnNldFxuXHRsZXQgZm9yZWdyb3VuZEJhckdyb3VwID0gc3ZnXG5cdFx0LmFwcGVuZChcImdcIilcblx0XHQuYXR0cihcImZpbGxcIiwgZmlsbENvbG9yKTtcblxuXHQvLyBNaW4gYW5kIG1heCB2YWx1ZXMgbGFiZWxzXG5cdGNvbnN0IGF4ZXMgPSBzdmdcblx0XHQuYXBwZW5kKFwiZ1wiKVxuXHRcdC5hdHRyKFwidHJhbnNmb3JtXCIsIGB0cmFuc2xhdGUoMCwke2hlaWdodCAtIG1hcmdpbkJvdHRvbX0pYClcblx0XHQuY2FsbChcblx0XHRcdGQzXG5cdFx0XHRcdC5heGlzQm90dG9tKHgpXG5cdFx0XHRcdC50aWNrVmFsdWVzKFsuLi54LmRvbWFpbigpLCAwXSkgLy8gbWluL21heCB0aWNrcyBhbmQgaG92ZXJlZFxuXHRcdFx0XHQudGlja0Zvcm1hdCh0aWNrRm9ybWF0dGVyRm9yQmlucyh0eXBlLCBiaW5zKSlcblx0XHRcdFx0LnRpY2tTaXplKDIuNSksXG5cdFx0KVxuXHRcdC5jYWxsKChnKSA9PiB7XG5cdFx0XHRnLnNlbGVjdChcIi5kb21haW5cIikucmVtb3ZlKCk7XG5cdFx0XHRnLmF0dHIoXCJjbGFzc1wiLCBcImdyYXlcIik7XG5cdFx0XHRnLnNlbGVjdEFsbChcIi50aWNrIHRleHRcIilcblx0XHRcdFx0LmF0dHIoXCJ0ZXh0LWFuY2hvclwiLCAoXywgaSkgPT4gW1wic3RhcnRcIiwgXCJlbmRcIiwgXCJzdGFydFwiXVtpXSlcblx0XHRcdFx0LmF0dHIoXCJkeFwiLCAoXywgaSkgPT4gW1wiLTAuMjVlbVwiLCBcIjAuMjVlbVwiLCBcIi0wLjI1ZW1cIl1baV0pO1xuXHRcdH0pO1xuXG5cdGNvbnN0IGhvdmVyZWRUaWNrR3JvdXAgPSBheGVzLm5vZGUoKT8ucXVlcnlTZWxlY3RvckFsbChcIi50aWNrXCIpWzJdO1xuXHRhc3NlcnQoaG92ZXJlZFRpY2tHcm91cCwgXCJpbnZhcmlhbnRcIik7XG5cdGNvbnN0IGhvdmVyZWRUaWNrID0gZDMuc2VsZWN0KGhvdmVyZWRUaWNrR3JvdXApO1xuXG5cdC8vfiBCYWNrZ3JvdW5kIHJlY3QgZm9yIHRoZSBuZXh0IHNlY3Rpb24gKGhvdmVyIGxhYmVsKVxuXHRjb25zdCBob3ZlckxhYmVsQmFja2dyb3VuZCA9IGhvdmVyZWRUaWNrXG5cdFx0Lmluc2VydChcInJlY3RcIiwgXCI6Zmlyc3QtY2hpbGRcIilcblx0XHQuYXR0cihcIndpZHRoXCIsIDIwKVxuXHRcdC5hdHRyKFwiaGVpZ2h0XCIsIDIwKVxuXHRcdC5zdHlsZShcImZpbGxcIiwgXCJ3aGl0ZVwiKTtcblxuXHRjb25zdCBmbXQgPSB0eXBlID09PSBcIm51bWJlclwiXG5cdFx0PyBkMy5mb3JtYXQoXCIuM3NcIilcblx0XHQ6IHRpY2tGb3JtYXR0ZXJGb3JCaW5zKHR5cGUsIGJpbnMpO1xuXG5cdGxldCBbeG1pbiwgeG1heF0gPSB4LmRvbWFpbigpO1xuXHRlZmZlY3QoKCkgPT4ge1xuXHRcdGhvdmVyZWRUaWNrXG5cdFx0XHQuYXR0cihcInRyYW5zZm9ybVwiLCBgdHJhbnNsYXRlKCR7eChob3ZlcmVkLnZhbHVlID8/IHhtaW4pfSwwKWApXG5cdFx0XHQuYXR0cihcInZpc2liaWxpdHlcIiwgaG92ZXJlZC52YWx1ZSA/IFwidmlzaWJsZVwiIDogXCJoaWRkZW5cIik7XG5cblx0XHRob3ZlcmVkVGlja1xuXHRcdFx0LnNlbGVjdEFsbChcInRleHRcIilcblx0XHRcdC50ZXh0KGAke2ZtdChob3ZlcmVkLnZhbHVlID8/IHhtaW4pfWApXG5cdFx0XHQuYXR0cihcInZpc2liaWxpdHlcIiwgaG92ZXJlZC52YWx1ZSA/IFwidmlzaWJsZVwiIDogXCJoaWRkZW5cIik7XG5cblx0XHRjb25zdCBob3ZlcmVkVGlja1RleHQgPSBob3ZlcmVkVGlja1xuXHRcdFx0LnNlbGVjdChcInRleHRcIilcblx0XHRcdC5ub2RlKCkgYXMgU1ZHVGV4dEVsZW1lbnQ7XG5cdFx0Y29uc3QgYmJveCA9IGhvdmVyZWRUaWNrVGV4dC5nZXRCQm94KCk7XG5cdFx0Y29uc3QgY29uZCA9ICh4KGhvdmVyZWQudmFsdWUgPz8geG1pbikgKyBiYm94LndpZHRoKSA+IHgoeG1heCk7XG5cblx0XHRob3ZlcmVkVGlja1RleHQuc2V0QXR0cmlidXRlKFwidGV4dC1hbmNob3JcIiwgY29uZCA/IFwiZW5kXCIgOiBcInN0YXJ0XCIpO1xuXHRcdGhvdmVyZWRUaWNrVGV4dC5zZXRBdHRyaWJ1dGUoXCJkeFwiLCBjb25kID8gXCItMC4yNWVtXCIgOiBcIjAuMjVlbVwiKTtcblxuXHRcdGhvdmVyTGFiZWxCYWNrZ3JvdW5kXG5cdFx0XHQuYXR0cihcInZpc2liaWxpdHlcIiwgaG92ZXJlZC52YWx1ZSA/IFwidmlzaWJsZVwiIDogXCJoaWRkZW5cIilcblx0XHRcdC5hdHRyKFwidHJhbnNmb3JtXCIsIGB0cmFuc2xhdGUoJHsoY29uZCA/IC1iYm94LndpZHRoIDogMCkgLSAyLjV9LCAyLjUpYClcblx0XHRcdC5hdHRyKFwid2lkdGhcIiwgYmJveC53aWR0aCArIDUpXG5cdFx0XHQuYXR0cihcImhlaWdodFwiLCBiYm94LmhlaWdodCArIDUpO1xuXHR9KTtcblxuXHQvKiogQHR5cGUge3R5cGVvZiBmb3JlZ3JvdW5kQmFyR3JvdXAgfCB1bmRlZmluZWR9ICovXG5cdGxldCBmb3JlZ3JvdW5kTnVsbEdyb3VwOiB0eXBlb2YgZm9yZWdyb3VuZEJhckdyb3VwIHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkO1xuXHRpZiAobnVsbENvdW50ID4gMCkge1xuXHRcdGxldCB4bnVsbCA9IGQzLnNjYWxlTGluZWFyKClcblx0XHRcdC5yYW5nZShbbWFyZ2luTGVmdCwgbWFyZ2luTGVmdCArIG51bGxCaW5XaWR0aF0pO1xuXG5cdFx0Ly8gYmFja2dyb3VuZCBiYXIgZm9yIHRoZSBudWxsIGJpblxuXHRcdHN2Zy5hcHBlbmQoXCJnXCIpXG5cdFx0XHQuYXR0cihcImZpbGxcIiwgYmFja2dyb3VuZEJhckNvbG9yKVxuXHRcdFx0LmFwcGVuZChcInJlY3RcIilcblx0XHRcdC5hdHRyKFwieFwiLCB4bnVsbCgwKSlcblx0XHRcdC5hdHRyKFwid2lkdGhcIiwgeG51bGwoMSkgLSB4bnVsbCgwKSlcblx0XHRcdC5hdHRyKFwieVwiLCB5KG51bGxDb3VudCkpXG5cdFx0XHQuYXR0cihcImhlaWdodFwiLCB5KDApIC0geShudWxsQ291bnQpKTtcblxuXHRcdGZvcmVncm91bmROdWxsR3JvdXAgPSBzdmdcblx0XHRcdC5hcHBlbmQoXCJnXCIpXG5cdFx0XHQuYXR0cihcImZpbGxcIiwgbnVsbEZpbGxDb2xvcilcblx0XHRcdC5hdHRyKFwiY29sb3JcIiwgbnVsbEZpbGxDb2xvcik7XG5cblx0XHRmb3JlZ3JvdW5kTnVsbEdyb3VwLmFwcGVuZChcInJlY3RcIilcblx0XHRcdC5hdHRyKFwieFwiLCB4bnVsbCgwKSlcblx0XHRcdC5hdHRyKFwid2lkdGhcIiwgeG51bGwoMSkgLSB4bnVsbCgwKSk7XG5cblx0XHQvLyBBcHBlbmQgdGhlIHgtYXhpcyBhbmQgYWRkIGEgbnVsbCB0aWNrXG5cdFx0bGV0IGF4aXNHcm91cCA9IGZvcmVncm91bmROdWxsR3JvdXAuYXBwZW5kKFwiZ1wiKVxuXHRcdFx0LmF0dHIoXCJ0cmFuc2Zvcm1cIiwgYHRyYW5zbGF0ZSgwLCR7aGVpZ2h0IC0gbWFyZ2luQm90dG9tfSlgKVxuXHRcdFx0LmFwcGVuZChcImdcIilcblx0XHRcdC5hdHRyKFwidHJhbnNmb3JtXCIsIGB0cmFuc2xhdGUoJHt4bnVsbCgwLjUpfSwgMClgKVxuXHRcdFx0LmF0dHIoXCJjbGFzc1wiLCBcInRpY2tcIik7XG5cblx0XHRheGlzR3JvdXBcblx0XHRcdC5hcHBlbmQoXCJsaW5lXCIpXG5cdFx0XHQuYXR0cihcInN0cm9rZVwiLCBcImN1cnJlbnRDb2xvclwiKVxuXHRcdFx0LmF0dHIoXCJ5MlwiLCAyLjUpO1xuXG5cdFx0YXhpc0dyb3VwXG5cdFx0XHQuYXBwZW5kKFwidGV4dFwiKVxuXHRcdFx0LmF0dHIoXCJmaWxsXCIsIFwiY3VycmVudENvbG9yXCIpXG5cdFx0XHQuYXR0cihcInlcIiwgNC41KVxuXHRcdFx0LmF0dHIoXCJkeVwiLCBcIjAuNzFlbVwiKVxuXHRcdFx0LmF0dHIoXCJ0ZXh0LWFuY2hvclwiLCBcIm1pZGRsZVwiKVxuXHRcdFx0LnRleHQoXCJcdTIyMDVcIilcblx0XHRcdC5hdHRyKFwiZm9udC1zaXplXCIsIFwiMC45ZW1cIilcblx0XHRcdC5hdHRyKFwiZm9udC1mYW1pbHlcIiwgXCJ2YXIoLS1zYW5zLXNlcmlmKVwiKVxuXHRcdFx0LmF0dHIoXCJmb250LXdlaWdodFwiLCBcIm5vcm1hbFwiKTtcblx0fVxuXG5cdC8vIEFwcGx5IHN0eWxlcyBmb3IgYWxsIGF4aXMgdGlja3Ncblx0c3ZnLnNlbGVjdEFsbChcIi50aWNrXCIpXG5cdFx0LmF0dHIoXCJmb250LWZhbWlseVwiLCBcInZhcigtLXNhbnMtc2VyaWYpXCIpXG5cdFx0LmF0dHIoXCJmb250LXdlaWdodFwiLCBcIm5vcm1hbFwiKTtcblxuXHQvKipcblx0ICogQHBhcmFtIHtBcnJheTxCaW4+fSBiaW5zXG5cdCAqIEBwYXJhbSB7bnVtYmVyfSBudWxsQ291bnRcblx0ICovXG5cdGZ1bmN0aW9uIHJlbmRlcihiaW5zOiBBcnJheTxCaW4+LCBudWxsQ291bnQ6IG51bWJlcikge1xuXHRcdGZvcmVncm91bmRCYXJHcm91cFxuXHRcdFx0LnNlbGVjdEFsbChcInJlY3RcIilcblx0XHRcdC5kYXRhKGJpbnMpXG5cdFx0XHQuam9pbihcInJlY3RcIilcblx0XHRcdC5hdHRyKFwieFwiLCAoZCkgPT4geChkLngwKSArIDEuNSlcblx0XHRcdC5hdHRyKFwid2lkdGhcIiwgKGQpID0+IHgoZC54MSkgLSB4KGQueDApIC0gMS41KVxuXHRcdFx0LmF0dHIoXCJ5XCIsIChkKSA9PiB5KGQubGVuZ3RoKSlcblx0XHRcdC5hdHRyKFwiaGVpZ2h0XCIsIChkKSA9PiB5KDApIC0geShkLmxlbmd0aCkpO1xuXHRcdGZvcmVncm91bmROdWxsR3JvdXBcblx0XHRcdD8uc2VsZWN0KFwicmVjdFwiKVxuXHRcdFx0LmF0dHIoXCJ5XCIsIHkobnVsbENvdW50KSlcblx0XHRcdC5hdHRyKFwiaGVpZ2h0XCIsIHkoMCkgLSB5KG51bGxDb3VudCkpO1xuXHR9XG5cblx0bGV0IHNjYWxlcyA9IHtcblx0XHR4OiBPYmplY3QuYXNzaWduKHgsIHtcblx0XHRcdHR5cGU6IFwibGluZWFyXCIsXG5cdFx0XHRkb21haW46IHguZG9tYWluKCksXG5cdFx0XHRyYW5nZTogeC5yYW5nZSgpLFxuXHRcdH0pLFxuXHRcdHk6IE9iamVjdC5hc3NpZ24oeSwge1xuXHRcdFx0dHlwZTogXCJsaW5lYXJcIixcblx0XHRcdGRvbWFpbjogeS5kb21haW4oKSxcblx0XHRcdHJhbmdlOiB5LnJhbmdlKCksXG5cdFx0fSksXG5cdH07XG5cdGxldCBub2RlID0gc3ZnLm5vZGUoKTtcblx0YXNzZXJ0KG5vZGUsIFwiSW5mYWxsYWJsZVwiKTtcblxuXHRub2RlLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZW1vdmVcIiwgKGV2ZW50KSA9PiB7XG5cdFx0Y29uc3QgcmVsYXRpdmVYID0gZXZlbnQuY2xpZW50WCAtIG5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkubGVmdDtcblx0XHRob3ZlcmVkLnZhbHVlID0gY2xhbXAoeC5pbnZlcnQocmVsYXRpdmVYKSwgeG1pbiwgeG1heCk7XG5cdH0pO1xuXHRub2RlLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZWxlYXZlXCIsICgpID0+IHtcblx0XHRob3ZlcmVkLnZhbHVlID0gdW5kZWZpbmVkO1xuXHR9KTtcblxuXHRyZW5kZXIoYmlucywgbnVsbENvdW50KTtcblx0cmV0dXJuIE9iamVjdC5hc3NpZ24obm9kZSwge1xuXHRcdC8qKiBAcGFyYW0ge3N0cmluZ30gdHlwZSAqL1xuXHRcdHNjYWxlKHR5cGU6IHN0cmluZykge1xuXHRcdFx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIHNjYWxlcyBpcyBub3QgZGVmaW5lZFxuXHRcdFx0bGV0IHNjYWxlID0gc2NhbGVzW3R5cGVdO1xuXHRcdFx0YXNzZXJ0KHNjYWxlLCBcIkludmFsaWQgc2NhbGUgdHlwZVwiKTtcblx0XHRcdHJldHVybiBzY2FsZTtcblx0XHR9LFxuXHRcdC8qKlxuXHRcdCAqIEBwYXJhbSB7QXJyYXk8QmluPn0gYmluc1xuXHRcdCAqIEBwYXJhbSB7eyBudWxsQ291bnQ6IG51bWJlciB9fSBvcHRzXG5cdFx0ICovXG5cdFx0dXBkYXRlKGJpbnM6IEFycmF5PEJpbj4sIHsgbnVsbENvdW50IH06IHsgbnVsbENvdW50OiBudW1iZXIgfSkge1xuXHRcdFx0cmVuZGVyKGJpbnMsIG51bGxDb3VudCk7XG5cdFx0fSxcblx0XHRyZXNldCgpIHtcblx0XHRcdHJlbmRlcihiaW5zLCBudWxsQ291bnQpO1xuXHRcdH0sXG5cdH0pO1xufVxuXG5mdW5jdGlvbiBjbGFtcChcblx0dmFsdWU6IG51bWJlciB8IERhdGUsXG5cdG1pbjogbnVtYmVyIHwgRGF0ZSxcblx0bWF4OiBudW1iZXIgfCBEYXRlLFxuKTogbnVtYmVyIHtcblx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIHZhbHVlIGlzIGVpdGhlciBudW1iZXIgb3IgRGF0ZVxuXHRyZXR1cm4gTWF0aC5tYXgobWluLCBNYXRoLm1pbihtYXgsIHZhbHVlKSk7XG59XG4iLCAiLy8gVGhlIHR5cGVzIGZvciBkMyBhcmUgcmVhbGx5IGFubm95aW5nLlxuXG4vLyBAZGVuby10eXBlcz1cIm5wbTpAdHlwZXMvZDMtc2VsZWN0aW9uQDNcIlxuZXhwb3J0ICogZnJvbSBcImQzLXNlbGVjdGlvblwiO1xuLy8gQGRlbm8tdHlwZXM9XCJucG06QHR5cGVzL2QzLXNjYWxlQDRcIlxuZXhwb3J0ICogZnJvbSBcImQzLXNjYWxlXCI7XG4vLyBAZGVuby10eXBlcz1cIm5wbTpAdHlwZXMvZDMtYXhpc0AzXCJcbmV4cG9ydCAqIGZyb20gXCJkMy1heGlzXCI7XG4vLyBAZGVuby10eXBlcz1cIm5wbTpAdHlwZXMvZDMtZm9ybWF0QDNcIlxuZXhwb3J0ICogZnJvbSBcImQzLWZvcm1hdFwiO1xuLy8gQGRlbm8tdHlwZXM9XCJucG06QHR5cGVzL2QzLXRpbWUtZm9ybWF0QDRcIlxuZXhwb3J0ICogZnJvbSBcImQzLXRpbWUtZm9ybWF0XCI7XG4iLCAiaW1wb3J0ICogYXMgZDMgZnJvbSBcIi4uL2RlcHMvZDMudHNcIjtcbmltcG9ydCB0eXBlIHsgQmluIH0gZnJvbSBcIi4uL3R5cGVzLnRzXCI7XG5cbmxldCBZRUFSID0gXCJ5ZWFyXCI7XG5sZXQgTU9OVEggPSBcIm1vbnRoXCI7XG5sZXQgREFZID0gXCJkYXlcIjtcbmxldCBIT1VSID0gXCJob3VyXCI7XG5sZXQgTUlOVVRFID0gXCJtaW51dGVcIjtcbmxldCBTRUNPTkQgPSBcInNlY29uZFwiO1xubGV0IE1JTExJU0VDT05EID0gXCJtaWxsaXNlY29uZFwiO1xuXG5sZXQgZHVyYXRpb25TZWNvbmQgPSAxMDAwO1xubGV0IGR1cmF0aW9uTWludXRlID0gZHVyYXRpb25TZWNvbmQgKiA2MDtcbmxldCBkdXJhdGlvbkhvdXIgPSBkdXJhdGlvbk1pbnV0ZSAqIDYwO1xubGV0IGR1cmF0aW9uRGF5ID0gZHVyYXRpb25Ib3VyICogMjQ7XG5sZXQgZHVyYXRpb25XZWVrID0gZHVyYXRpb25EYXkgKiA3O1xubGV0IGR1cmF0aW9uTW9udGggPSBkdXJhdGlvbkRheSAqIDMwO1xubGV0IGR1cmF0aW9uWWVhciA9IGR1cmF0aW9uRGF5ICogMzY1O1xuXG5sZXQgaW50ZXJ2YWxzID0gW1xuXHRbU0VDT05ELCAxLCBkdXJhdGlvblNlY29uZF0sXG5cdFtTRUNPTkQsIDUsIDUgKiBkdXJhdGlvblNlY29uZF0sXG5cdFtTRUNPTkQsIDE1LCAxNSAqIGR1cmF0aW9uU2Vjb25kXSxcblx0W1NFQ09ORCwgMzAsIDMwICogZHVyYXRpb25TZWNvbmRdLFxuXHRbTUlOVVRFLCAxLCBkdXJhdGlvbk1pbnV0ZV0sXG5cdFtNSU5VVEUsIDUsIDUgKiBkdXJhdGlvbk1pbnV0ZV0sXG5cdFtNSU5VVEUsIDE1LCAxNSAqIGR1cmF0aW9uTWludXRlXSxcblx0W01JTlVURSwgMzAsIDMwICogZHVyYXRpb25NaW51dGVdLFxuXHRbSE9VUiwgMSwgZHVyYXRpb25Ib3VyXSxcblx0W0hPVVIsIDMsIDMgKiBkdXJhdGlvbkhvdXJdLFxuXHRbSE9VUiwgNiwgNiAqIGR1cmF0aW9uSG91cl0sXG5cdFtIT1VSLCAxMiwgMTIgKiBkdXJhdGlvbkhvdXJdLFxuXHRbREFZLCAxLCBkdXJhdGlvbkRheV0sXG5cdFtEQVksIDcsIGR1cmF0aW9uV2Vla10sXG5cdFtNT05USCwgMSwgZHVyYXRpb25Nb250aF0sXG5cdFtNT05USCwgMywgMyAqIGR1cmF0aW9uTW9udGhdLFxuXHRbWUVBUiwgMSwgZHVyYXRpb25ZZWFyXSxcbl0gYXMgY29uc3Q7XG5cbmxldCBmb3JtYXRNYXAgPSB7XG5cdFtNSUxMSVNFQ09ORF06IGQzLnRpbWVGb3JtYXQoXCIlTFwiKSxcblx0W1NFQ09ORF06IGQzLnRpbWVGb3JtYXQoXCIlUyBzXCIpLFxuXHRbTUlOVVRFXTogZDMudGltZUZvcm1hdChcIiVIOiVNXCIpLFxuXHRbSE9VUl06IGQzLnRpbWVGb3JtYXQoXCIlSDolTVwiKSxcblx0W0RBWV06IGQzLnRpbWVGb3JtYXQoXCIlYiAlZFwiKSxcblx0W01PTlRIXTogZDMudGltZUZvcm1hdChcIiViICVZXCIpLFxuXHRbWUVBUl06IGQzLnRpbWVGb3JtYXQoXCIlWVwiKSxcbn07XG5cbi8qKlxuICogQHBhcmFtIHR5cGUgLSB0aGUgdHlwZSBvZiBkYXRhIGFzIGEgSmF2YVNjcmlwdCBwcmltaXRpdmVcbiAqIEBwYXJhbSBiaW5zIC0gdGhlIGJpbiBkYXRhIHRoYXQgbmVlZHMgdG8gYmUgZm9ybWF0dGVkXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiB0aWNrRm9ybWF0dGVyRm9yQmlucyhcblx0dHlwZTogXCJkYXRlXCIgfCBcIm51bWJlclwiLFxuXHRiaW5zOiBBcnJheTxCaW4+LFxuKTogKGQ6IGQzLk51bWJlclZhbHVlKSA9PiBzdHJpbmcge1xuXHRpZiAodHlwZSA9PT0gXCJudW1iZXJcIikge1xuXHRcdHJldHVybiBkMy5mb3JtYXQoXCJ+c1wiKTtcblx0fVxuXHRsZXQgaW50ZXJ2YWwgPSB0aW1lSW50ZXJ2YWwoXG5cdFx0Ymluc1swXS54MCxcblx0XHRiaW5zW2JpbnMubGVuZ3RoIC0gMV0ueDEsXG5cdFx0Ymlucy5sZW5ndGgsXG5cdCk7XG5cdC8vIEB0cy1leHBlY3QtZXJyb3IgLSBkMyBvayB3aXRoIGRhdGUgLT4gc3RyaW5nIGFzIGxvbmcgYXMgaXQncyB1dGNcblx0cmV0dXJuIGZvcm1hdE1hcFtpbnRlcnZhbC5pbnRlcnZhbF07XG59XG5cbi8vLyBiaW4gc3R1ZmYgZnJvbSB2Z3Bsb3RcblxuLyoqXG4gKiBAcGFyYW0gbWluXG4gKiBAcGFyYW0gbWF4XG4gKiBAcGFyYW0gc3RlcHNcbiAqL1xuZnVuY3Rpb24gdGltZUludGVydmFsKFxuXHRtaW46IG51bWJlcixcblx0bWF4OiBudW1iZXIsXG5cdHN0ZXBzOiBudW1iZXIsXG4pOiB7XG5cdGludGVydmFsOiB0eXBlb2YgaW50ZXJ2YWxzW251bWJlcl1bMF0gfCB0eXBlb2YgTUlMTElTRUNPTkQ7XG5cdHN0ZXA6IG51bWJlcjtcbn0ge1xuXHRjb25zdCBzcGFuID0gbWF4IC0gbWluO1xuXHRjb25zdCB0YXJnZXQgPSBzcGFuIC8gc3RlcHM7XG5cblx0bGV0IGkgPSAwO1xuXHR3aGlsZSAoaSA8IGludGVydmFscy5sZW5ndGggJiYgaW50ZXJ2YWxzW2ldWzJdIDwgdGFyZ2V0KSB7XG5cdFx0aSsrO1xuXHR9XG5cblx0aWYgKGkgPT09IGludGVydmFscy5sZW5ndGgpIHtcblx0XHRyZXR1cm4geyBpbnRlcnZhbDogWUVBUiwgc3RlcDogYmluU3RlcChzcGFuLCBzdGVwcykgfTtcblx0fVxuXG5cdGlmIChpID4gMCkge1xuXHRcdGxldCBpbnRlcnZhbCA9IGludGVydmFsc1tcblx0XHRcdHRhcmdldCAvIGludGVydmFsc1tpIC0gMV1bMl0gPCBpbnRlcnZhbHNbaV1bMl0gLyB0YXJnZXQgPyBpIC0gMSA6IGlcblx0XHRdO1xuXHRcdHJldHVybiB7IGludGVydmFsOiBpbnRlcnZhbFswXSwgc3RlcDogaW50ZXJ2YWxbMV0gfTtcblx0fVxuXG5cdHJldHVybiB7IGludGVydmFsOiBNSUxMSVNFQ09ORCwgc3RlcDogYmluU3RlcChzcGFuLCBzdGVwcywgMSkgfTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge251bWJlcn0gc3BhblxuICogQHBhcmFtIHtudW1iZXJ9IHN0ZXBzXG4gKiBAcGFyYW0ge251bWJlcn0gW21pbnN0ZXBdXG4gKiBAcGFyYW0ge251bWJlcn0gW2xvZ2JdXG4gKi9cbmZ1bmN0aW9uIGJpblN0ZXAoXG5cdHNwYW46IG51bWJlcixcblx0c3RlcHM6IG51bWJlcixcblx0bWluc3RlcDogbnVtYmVyID0gMCxcblx0bG9nYjogbnVtYmVyID0gTWF0aC5MTjEwLFxuKSB7XG5cdGxldCB2O1xuXG5cdGNvbnN0IGxldmVsID0gTWF0aC5jZWlsKE1hdGgubG9nKHN0ZXBzKSAvIGxvZ2IpO1xuXHRsZXQgc3RlcCA9IE1hdGgubWF4KFxuXHRcdG1pbnN0ZXAsXG5cdFx0TWF0aC5wb3coMTAsIE1hdGgucm91bmQoTWF0aC5sb2coc3BhbikgLyBsb2diKSAtIGxldmVsKSxcblx0KTtcblxuXHQvLyBpbmNyZWFzZSBzdGVwIHNpemUgaWYgdG9vIG1hbnkgYmluc1xuXHR3aGlsZSAoTWF0aC5jZWlsKHNwYW4gLyBzdGVwKSA+IHN0ZXBzKSBzdGVwICo9IDEwO1xuXG5cdC8vIGRlY3JlYXNlIHN0ZXAgc2l6ZSBpZiBhbGxvd2VkXG5cdGNvbnN0IGRpdiA9IFs1LCAyXTtcblx0Zm9yIChsZXQgaSA9IDAsIG4gPSBkaXYubGVuZ3RoOyBpIDwgbjsgKytpKSB7XG5cdFx0diA9IHN0ZXAgLyBkaXZbaV07XG5cdFx0aWYgKHYgPj0gbWluc3RlcCAmJiBzcGFuIC8gdiA8PSBzdGVwcykgc3RlcCA9IHY7XG5cdH1cblxuXHRyZXR1cm4gc3RlcDtcbn1cbiIsICIvLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLWNvcmUuZC50c1wiO1xuaW1wb3J0IHsgY2xhdXNlUG9pbnQsIE1vc2FpY0NsaWVudCwgdHlwZSBTZWxlY3Rpb24gfSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtY29yZVwiO1xuLy8gQGRlbm8tdHlwZXM9XCIuLi9kZXBzL21vc2FpYy1zcWwuZC50c1wiO1xuaW1wb3J0IHtcblx0Y29sdW1uLFxuXHRjb3VudCxcblx0UXVlcnksXG5cdHNxbCxcblx0U1FMRXhwcmVzc2lvbixcblx0c3VtLFxufSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtc3FsXCI7XG5pbXBvcnQgdHlwZSAqIGFzIGFycm93IGZyb20gXCJhcGFjaGUtYXJyb3dcIjtcbmltcG9ydCB7IGVmZmVjdCB9IGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuXG5pbXBvcnQgeyBWYWx1ZUNvdW50c1Bsb3QgfSBmcm9tIFwiLi4vdXRpbHMvVmFsdWVDb3VudHNQbG90LnRzXCI7XG5pbXBvcnQgeyBhc3NlcnQgfSBmcm9tIFwiLi4vdXRpbHMvYXNzZXJ0LnRzXCI7XG5cbmludGVyZmFjZSBVbmlxdWVWYWx1ZXNPcHRpb25zIHtcblx0LyoqIFRoZSB0YWJsZSB0byBxdWVyeS4gKi9cblx0dGFibGU6IHN0cmluZztcblx0LyoqIFRoZSBjb2x1bW4gdG8gdXNlIGZvciB0aGUgaGlzdG9ncmFtLiAqL1xuXHRjb2x1bW46IHN0cmluZztcblx0LyoqIEEgbW9zYWljIHNlbGVjdGlvbiB0byBmaWx0ZXIgdGhlIGRhdGEuICovXG5cdGZpbHRlckJ5OiBTZWxlY3Rpb247XG59XG5cbnR5cGUgQ291bnRUYWJsZSA9IGFycm93LlRhYmxlPHsga2V5OiBhcnJvdy5VdGY4OyB0b3RhbDogYXJyb3cuSW50IH0+O1xuXG5leHBvcnQgY2xhc3MgVmFsdWVDb3VudHMgZXh0ZW5kcyBNb3NhaWNDbGllbnQge1xuXHQjdGFibGU6IHN0cmluZztcblx0I2NvbHVtbjogc3RyaW5nO1xuXHQjZWw6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0I3Bsb3Q6IFJldHVyblR5cGU8dHlwZW9mIFZhbHVlQ291bnRzUGxvdD4gfCB1bmRlZmluZWQ7XG5cblx0Y29uc3RydWN0b3Iob3B0aW9uczogVW5pcXVlVmFsdWVzT3B0aW9ucykge1xuXHRcdHN1cGVyKG9wdGlvbnMuZmlsdGVyQnkpO1xuXHRcdHRoaXMuI3RhYmxlID0gb3B0aW9ucy50YWJsZTtcblx0XHR0aGlzLiNjb2x1bW4gPSBvcHRpb25zLmNvbHVtbjtcblxuXHRcdC8vIEZJWE1FOiBUaGVyZSBpcyBzb21lIGlzc3VlIHdpdGggdGhlIG1vc2FpYyBjbGllbnQgb3IgdGhlIHF1ZXJ5IHdlXG5cdFx0Ly8gYXJlIHVzaW5nIGhlcmUuIFVwZGF0ZXMgdG8gdGhlIFNlbGVjdGlvbiAoYGZpbHRlckJ5YCkgc2VlbSB0byBiZVxuXHRcdC8vIG1pc3NlZCBieSB0aGUgY29vcmRpbmF0b3IsIGFuZCBxdWVyeS9xdWVyeVJlc3VsdCBhcmUgbm90IGNhbGxlZFxuXHRcdC8vIGJ5IHRoZSBjb29yZGluYXRvciB3aGVuIHRoZSBmaWx0ZXJCeSBpcyB1cGRhdGVkLlxuXHRcdC8vXG5cdFx0Ly8gSGVyZSB3ZSBtYW51YWxseSBsaXN0ZW4gZm9yIHRoZSBjaGFuZ2VzIHRvIGZpbHRlckJ5IGFuZCB1cGRhdGUgdGhpc1xuXHRcdC8vIGNsaWVudCBpbnRlcm5hbGx5LiBJdCBfc2hvdWxkXyBnbyB0aHJvdWdoIHRoZSBjb29yZGluYXRvci5cblx0XHRvcHRpb25zLmZpbHRlckJ5LmFkZEV2ZW50TGlzdGVuZXIoXCJ2YWx1ZVwiLCBhc3luYyAoKSA9PiB7XG5cdFx0XHRsZXQgZmlsdGVycyA9IG9wdGlvbnMuZmlsdGVyQnkucHJlZGljYXRlKCk7XG5cdFx0XHRsZXQgcXVlcnkgPSB0aGlzLnF1ZXJ5KGZpbHRlcnMpO1xuXHRcdFx0aWYgKHRoaXMuI3Bsb3QpIHtcblx0XHRcdFx0bGV0IGRhdGEgPSBhd2FpdCB0aGlzLmNvb3JkaW5hdG9yLnF1ZXJ5KHF1ZXJ5KTtcblx0XHRcdFx0dGhpcy4jcGxvdC5kYXRhLnZhbHVlID0gZGF0YTtcblx0XHRcdH1cblx0XHR9KTtcblx0fVxuXG5cdHF1ZXJ5KGZpbHRlcjogQXJyYXk8U1FMRXhwcmVzc2lvbj4gPSBbXSk6IFF1ZXJ5IHtcblx0XHRsZXQgY291bnRzID0gUXVlcnlcblx0XHRcdC5mcm9tKHsgc291cmNlOiB0aGlzLiN0YWJsZSB9KVxuXHRcdFx0LnNlbGVjdCh7XG5cdFx0XHRcdHZhbHVlOiBzcWxgQ0FTRVxuXHRcdFx0XHRcdFdIRU4gJHtjb2x1bW4odGhpcy4jY29sdW1uKX0gSVMgTlVMTCBUSEVOICdfX3F1YWtfbnVsbF9fJ1xuXHRcdFx0XHRcdEVMU0UgJHtjb2x1bW4odGhpcy4jY29sdW1uKX1cblx0XHRcdFx0RU5EYCxcblx0XHRcdFx0Y291bnQ6IGNvdW50KCksXG5cdFx0XHR9KVxuXHRcdFx0Lmdyb3VwYnkoXCJ2YWx1ZVwiKVxuXHRcdFx0LndoZXJlKGZpbHRlcik7XG5cdFx0cmV0dXJuIFF1ZXJ5XG5cdFx0XHQud2l0aCh7IGNvdW50cyB9KVxuXHRcdFx0LnNlbGVjdChcblx0XHRcdFx0e1xuXHRcdFx0XHRcdGtleTogc3FsYENBU0Vcblx0XHRcdFx0XHRcdFdIRU4gXCJjb3VudFwiID0gMSBBTkQgXCJ2YWx1ZVwiICE9ICdfX3F1YWtfbnVsbF9fJyBUSEVOICdfX3F1YWtfdW5pcXVlX18nXG5cdFx0XHRcdFx0XHRFTFNFIFwidmFsdWVcIlxuXHRcdFx0XHRcdEVORGAsXG5cdFx0XHRcdFx0dG90YWw6IHN1bShcImNvdW50XCIpLFxuXHRcdFx0XHR9LFxuXHRcdFx0KVxuXHRcdFx0LmZyb20oXCJjb3VudHNcIilcblx0XHRcdC5ncm91cGJ5KFwia2V5XCIpO1xuXHR9XG5cblx0cXVlcnlSZXN1bHQoZGF0YTogQ291bnRUYWJsZSk6IHRoaXMge1xuXHRcdGlmICghdGhpcy4jcGxvdCkge1xuXHRcdFx0bGV0IHBsb3QgPSB0aGlzLiNwbG90ID0gVmFsdWVDb3VudHNQbG90KGRhdGEpO1xuXHRcdFx0dGhpcy4jZWwuYXBwZW5kQ2hpbGQocGxvdCk7XG5cdFx0XHRlZmZlY3QoKCkgPT4ge1xuXHRcdFx0XHRsZXQgY2xhdXNlID0gdGhpcy5jbGF1c2UocGxvdC5zZWxlY3RlZC52YWx1ZSk7XG5cdFx0XHRcdHRoaXMuZmlsdGVyQnkhLnVwZGF0ZShjbGF1c2UpO1xuXHRcdFx0fSk7XG5cdFx0fSBlbHNlIHtcblx0XHRcdHRoaXMuI3Bsb3QuZGF0YS52YWx1ZSA9IGRhdGE7XG5cdFx0fVxuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cblx0Y2xhdXNlPFQ+KHZhbHVlPzogVCkge1xuXHRcdGxldCB1cGRhdGUgPSB2YWx1ZSA9PT0gXCJfX3F1YWtfbnVsbF9fXCIgPyBudWxsIDogdmFsdWU7XG5cdFx0cmV0dXJuIGNsYXVzZVBvaW50KHRoaXMuI2NvbHVtbiwgdXBkYXRlLCB7XG5cdFx0XHRzb3VyY2U6IHRoaXMsXG5cdFx0fSk7XG5cdH1cblxuXHRyZXNldCgpIHtcblx0XHRhc3NlcnQodGhpcy4jcGxvdCwgXCJWYWx1ZUNvdW50cyBwbG90IG5vdCBpbml0aWFsaXplZFwiKTtcblx0XHR0aGlzLiNwbG90LnNlbGVjdGVkLnZhbHVlID0gdW5kZWZpbmVkO1xuXHR9XG5cblx0Z2V0IHBsb3QoKSB7XG5cdFx0cmV0dXJuIHtcblx0XHRcdG5vZGU6ICgpID0+IHRoaXMuI2VsLFxuXHRcdH07XG5cdH1cbn1cbiIsICJpbXBvcnQgeyBlZmZlY3QsIHNpZ25hbCB9IGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuaW1wb3J0IHR5cGUgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG5pbXBvcnQgKiBhcyBkMyBmcm9tIFwiLi4vZGVwcy9kMy50c1wiO1xuaW1wb3J0IHsgYXNzZXJ0IH0gZnJvbSBcIi4vYXNzZXJ0LnRzXCI7XG5cbnR5cGUgQ291bnRUYWJsZURhdGEgPSBhcnJvdy5UYWJsZTx7XG5cdGtleTogYXJyb3cuVXRmODtcblx0dG90YWw6IGFycm93LkludDtcbn0+O1xuXG5pbnRlcmZhY2UgVmFsdWVDb3VudHNQbG90IHtcblx0d2lkdGg/OiBudW1iZXI7XG5cdGhlaWdodD86IG51bWJlcjtcblx0bWFyZ2luUmlnaHQ/OiBudW1iZXI7XG5cdG1hcmdpbkJvdHRvbT86IG51bWJlcjtcblx0bWFyZ2luTGVmdD86IG51bWJlcjtcblx0bnVsbENvdW50PzogbnVtYmVyO1xuXHRmaWxsQ29sb3I/OiBzdHJpbmc7XG5cdG51bGxGaWxsQ29sb3I/OiBzdHJpbmc7XG5cdGJhY2tncm91bmRCYXJDb2xvcj86IHN0cmluZztcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIFZhbHVlQ291bnRzUGxvdChcblx0ZGF0YTogQ291bnRUYWJsZURhdGEsXG5cdHtcblx0XHR3aWR0aCA9IDEyNSxcblx0XHRoZWlnaHQgPSAzMCxcblx0XHRtYXJnaW5Cb3R0b20gPSAxMixcblx0XHRtYXJnaW5SaWdodCA9IDIsXG5cdFx0bWFyZ2luTGVmdCA9IDIsXG5cdFx0ZmlsbENvbG9yID0gXCJ2YXIoLS1wcmltYXJ5KVwiLFxuXHRcdG51bGxGaWxsQ29sb3IgPSBcInZhcigtLXNlY29uZGFyeSlcIixcblx0XHRiYWNrZ3JvdW5kQmFyQ29sb3IgPSBcInJnYigyMjYsIDIyNiwgMjI2KVwiLFxuXHR9OiBWYWx1ZUNvdW50c1Bsb3QgPSB7fSxcbikge1xuXHRsZXQgcm9vdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdHJvb3Quc3R5bGUucG9zaXRpb24gPSBcInJlbGF0aXZlXCI7XG5cblx0bGV0IGNvbnRhaW5lciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdE9iamVjdC5hc3NpZ24oY29udGFpbmVyLnN0eWxlLCB7XG5cdFx0d2lkdGg6IGAke3dpZHRofXB4YCxcblx0XHRoZWlnaHQ6IGAke2hlaWdodH1weGAsXG5cdFx0ZGlzcGxheTogXCJmbGV4XCIsXG5cdFx0Ym9yZGVyUmFkaXVzOiBcIjVweFwiLFxuXHRcdG92ZXJmbG93OiBcImhpZGRlblwiLFxuXHR9KTtcblxuXHRsZXQgYmFycyA9IGNyZWF0ZUJhcnMoZGF0YSwge1xuXHRcdHdpZHRoLFxuXHRcdGhlaWdodCxcblx0XHRtYXJnaW5SaWdodCxcblx0XHRtYXJnaW5MZWZ0LFxuXHRcdGZpbGxDb2xvcixcblx0XHRudWxsRmlsbENvbG9yLFxuXHRcdGJhY2tncm91bmRCYXJDb2xvcixcblx0fSk7XG5cblx0Zm9yIChsZXQgYmFyIG9mIGJhcnMuZWxlbWVudHMpIHtcblx0XHRjb250YWluZXIuYXBwZW5kQ2hpbGQoYmFyKTtcblx0fVxuXG5cdGxldCB0ZXh0ID0gY3JlYXRlVGV4dE91dHB1dCgpO1xuXG5cdGxldCBob3ZlcmluZyA9IHNpZ25hbDxzdHJpbmcgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZCk7XG5cdGxldCBzZWxlY3RlZCA9IHNpZ25hbDxzdHJpbmcgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZCk7XG5cdGxldCBjb3VudHMgPSBzaWduYWw8Q291bnRUYWJsZURhdGE+KGRhdGEpO1xuXG5cdGxldCBoaXRBcmVhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0T2JqZWN0LmFzc2lnbihoaXRBcmVhLnN0eWxlLCB7XG5cdFx0cG9zaXRpb246IFwiYWJzb2x1dGVcIixcblx0XHR0b3A6IFwiMFwiLFxuXHRcdGxlZnQ6IFwiLTVweFwiLFxuXHRcdHdpZHRoOiBgJHt3aWR0aCArIDEwfXB4YCxcblx0XHRoZWlnaHQ6IGAke2hlaWdodCArIG1hcmdpbkJvdHRvbX1weGAsXG5cdFx0YmFja2dyb3VuZENvbG9yOiBcInJnYmEoMjU1LCAyNTUsIDI1NSwgMC4wMSlcIixcblx0XHRjdXJzb3I6IFwicG9pbnRlclwiLFxuXHR9KTtcblx0aGl0QXJlYS5hZGRFdmVudExpc3RlbmVyKFwibW91c2Vtb3ZlXCIsIChldmVudCkgPT4ge1xuXHRcdGhvdmVyaW5nLnZhbHVlID0gYmFycy5uZWFyZXN0WChldmVudCk7XG5cdH0pO1xuXHRoaXRBcmVhLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZW91dFwiLCAoKSA9PiB7XG5cdFx0aG92ZXJpbmcudmFsdWUgPSB1bmRlZmluZWQ7XG5cdH0pO1xuXHRoaXRBcmVhLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZWRvd25cIiwgKGV2ZW50KSA9PiB7XG5cdFx0bGV0IG5leHQgPSBiYXJzLm5lYXJlc3RYKGV2ZW50KTtcblx0XHRzZWxlY3RlZC52YWx1ZSA9IHNlbGVjdGVkLnZhbHVlID09PSBuZXh0ID8gdW5kZWZpbmVkIDogbmV4dDtcblx0fSk7XG5cblx0ZWZmZWN0KCgpID0+IHtcblx0XHR0ZXh0LnRleHRDb250ZW50ID0gYmFycy50ZXh0Rm9yKGhvdmVyaW5nLnZhbHVlID8/IHNlbGVjdGVkLnZhbHVlKTtcblx0XHRiYXJzLnJlbmRlcihjb3VudHMudmFsdWUsIGhvdmVyaW5nLnZhbHVlLCBzZWxlY3RlZC52YWx1ZSk7XG5cdH0pO1xuXG5cdHJvb3QuYXBwZW5kQ2hpbGQoY29udGFpbmVyKTtcblx0cm9vdC5hcHBlbmRDaGlsZCh0ZXh0KTtcblx0cm9vdC5hcHBlbmRDaGlsZChoaXRBcmVhKTtcblxuXHRyZXR1cm4gT2JqZWN0LmFzc2lnbihyb290LCB7IHNlbGVjdGVkLCBkYXRhOiBjb3VudHMgfSk7XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZUJhcihvcHRzOiB7XG5cdHRpdGxlOiBzdHJpbmc7XG5cdGZpbGxDb2xvcjogc3RyaW5nO1xuXHR0ZXh0Q29sb3I6IHN0cmluZztcblx0aGVpZ2h0OiBudW1iZXI7XG5cdHdpZHRoOiBudW1iZXI7XG59KSB7XG5cdGxldCB7IHRpdGxlLCBmaWxsQ29sb3IsIHRleHRDb2xvciwgd2lkdGgsIGhlaWdodCB9ID0gb3B0cztcblx0bGV0IGJhciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdGJhci50aXRsZSA9IHRpdGxlO1xuXHRPYmplY3QuYXNzaWduKGJhci5zdHlsZSwge1xuXHRcdGJhY2tncm91bmQ6IGNyZWF0ZVNwbGl0QmFyRmlsbCh7XG5cdFx0XHRjb2xvcjogZmlsbENvbG9yLFxuXHRcdFx0YmdDb2xvcjogXCJ2YXIoLS1tb29uLWdyYXkpXCIsXG5cdFx0XHRmcmFjOiA1MCxcblx0XHR9KSxcblx0XHR3aWR0aDogYCR7d2lkdGh9cHhgLFxuXHRcdGhlaWdodDogYCR7aGVpZ2h0fXB4YCxcblx0XHRib3JkZXJDb2xvcjogXCJ3aGl0ZVwiLFxuXHRcdGJvcmRlcldpZHRoOiBcIjBweCAxcHggMHB4IDBweFwiLFxuXHRcdGJvcmRlclN0eWxlOiBcInNvbGlkXCIsXG5cdFx0b3BhY2l0eTogMSxcblx0XHR0ZXh0QWxpZ246IFwiY2VudGVyXCIsXG5cdFx0cG9zaXRpb246IFwicmVsYXRpdmVcIixcblx0XHRkaXNwbGF5OiBcImZsZXhcIixcblx0XHRvdmVyZmxvdzogXCJoaWRkZW5cIixcblx0XHRhbGlnbkl0ZW1zOiBcImNlbnRlclwiLFxuXHRcdGZvbnRXZWlnaHQ6IDQwMCxcblx0XHRmb250RmFtaWx5OiBcInZhcigtLXNhbnMtc2VyaWYpXCIsXG5cdFx0Ym94U2l6aW5nOiBcImJvcmRlci1ib3hcIixcblx0fSk7XG5cdGxldCBzcGFuID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInNwYW5cIik7XG5cdE9iamVjdC5hc3NpZ24oc3Bhbi5zdHlsZSwge1xuXHRcdG92ZXJmbG93OiBcImhpZGRlblwiLFxuXHRcdHdpZHRoOiBgY2FsYygxMDAlIC0gNHB4KWAsXG5cdFx0bGVmdDogXCIwcHhcIixcblx0XHRwb3NpdGlvbjogXCJhYnNvbHV0ZVwiLFxuXHRcdHBhZGRpbmc6IFwiMHB4IDJweFwiLFxuXHRcdGNvbG9yOiB0ZXh0Q29sb3IsXG5cdH0pO1xuXHRpZiAod2lkdGggPiAxMCkge1xuXHRcdHNwYW4udGV4dENvbnRlbnQgPSB0aXRsZTtcblx0fVxuXHRiYXIuYXBwZW5kQ2hpbGQoc3Bhbik7XG5cdHJldHVybiBiYXI7XG59XG5cbmZ1bmN0aW9uIHByZXBhcmVEYXRhKGRhdGE6IENvdW50VGFibGVEYXRhKSB7XG5cdGxldCBhcnI6IEFycmF5PHsga2V5OiBzdHJpbmc7IHRvdGFsOiBudW1iZXIgfT4gPSBkYXRhXG5cdFx0LnRvQXJyYXkoKVxuXHRcdC50b1NvcnRlZCgoYSwgYikgPT4gYi50b3RhbCAtIGEudG90YWwpO1xuXHRsZXQgdG90YWwgPSBhcnIucmVkdWNlKChhY2MsIGQpID0+IGFjYyArIGQudG90YWwsIDApO1xuXHRyZXR1cm4ge1xuXHRcdGJpbnM6IGFyci5maWx0ZXIoKGQpID0+XG5cdFx0XHRkLmtleSAhPT0gXCJfX3F1YWtfbnVsbF9fXCIgJiYgZC5rZXkgIT09IFwiX19xdWFrX3VuaXF1ZV9fXCJcblx0XHQpLFxuXHRcdG51bGxDb3VudDogYXJyLmZpbmQoKGQpID0+IGQua2V5ID09PSBcIl9fcXVha19udWxsX19cIik/LnRvdGFsID8/IDAsXG5cdFx0dW5pcXVlQ291bnQ6IGFyci5maW5kKChkKSA9PiBkLmtleSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIik/LnRvdGFsID8/IDAsXG5cdFx0dG90YWwsXG5cdH07XG59XG5cbnR5cGUgRW50cnkgPSB7IGtleTogc3RyaW5nOyB0b3RhbDogbnVtYmVyIH07XG5cbmZ1bmN0aW9uIGNyZWF0ZUJhcnMoZGF0YTogQ291bnRUYWJsZURhdGEsIG9wdHM6IHtcblx0d2lkdGg6IG51bWJlcjtcblx0aGVpZ2h0OiBudW1iZXI7XG5cdG1hcmdpblJpZ2h0OiBudW1iZXI7XG5cdG1hcmdpbkxlZnQ6IG51bWJlcjtcblx0ZmlsbENvbG9yOiBzdHJpbmc7XG5cdGJhY2tncm91bmRCYXJDb2xvcjogc3RyaW5nO1xuXHRudWxsRmlsbENvbG9yOiBzdHJpbmc7XG59KSB7XG5cdGxldCBzb3VyY2UgPSBwcmVwYXJlRGF0YShkYXRhKTtcblx0bGV0IHggPSBkMy5zY2FsZUxpbmVhcigpXG5cdFx0LmRvbWFpbihbMCwgc291cmNlLnRvdGFsXSlcblx0XHQucmFuZ2UoW29wdHMubWFyZ2luTGVmdCwgb3B0cy53aWR0aCAtIG9wdHMubWFyZ2luUmlnaHRdKTtcblxuXHQvLyBudW1iZXIgb2YgYmFycyB0byBzaG93IGJlZm9yZSB2aXJ0dWFsaXppbmdcblx0bGV0IHRocmVzaCA9IDIwO1xuXG5cdGxldCBiYXJzOiBBcnJheTxIVE1MRWxlbWVudCAmIHsgZGF0YTogRW50cnkgfT4gPSBbXTtcblx0Zm9yIChsZXQgZCBvZiBzb3VyY2UuYmlucy5zbGljZSgwLCB0aHJlc2gpKSB7XG5cdFx0bGV0IGJhciA9IGNyZWF0ZUJhcih7XG5cdFx0XHR0aXRsZTogZC5rZXksXG5cdFx0XHRmaWxsQ29sb3I6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0dGV4dENvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHR3aWR0aDogeChkLnRvdGFsKSxcblx0XHRcdGhlaWdodDogb3B0cy5oZWlnaHQsXG5cdFx0fSk7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7IGRhdGE6IGQgfSkpO1xuXHR9XG5cblx0Ly8gVE9ETzogY3JlYXRlIGEgZGl2IFwiaG92ZXJcIiBiYXIgZm9yIHRoaXMgXCJhcmVhXCIgb2YgdGhlIHZpc3VhbGl6YXRpb25cblx0bGV0IGhvdmVyQmFyID0gY3JlYXRlVmlydHVhbFNlbGVjdGlvbkJhcihvcHRzKTtcblx0bGV0IHNlbGVjdEJhciA9IGNyZWF0ZVZpcnR1YWxTZWxlY3Rpb25CYXIob3B0cyk7XG5cdGxldCB2aXJ0dWFsQmFyOiBIVE1MRWxlbWVudCB8IHVuZGVmaW5lZDtcblx0aWYgKHNvdXJjZS5iaW5zLmxlbmd0aCA+IHRocmVzaCkge1xuXHRcdGxldCB0b3RhbCA9IHNvdXJjZS5iaW5zLnNsaWNlKHRocmVzaCkucmVkdWNlKFxuXHRcdFx0KGFjYywgZCkgPT4gYWNjICsgZC50b3RhbCxcblx0XHRcdDAsXG5cdFx0KTtcblx0XHR2aXJ0dWFsQmFyID0gT2JqZWN0LmFzc2lnbihkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpLCB7XG5cdFx0XHR0aXRsZTogXCJfX3F1YWtfdmlydHVhbF9fXCIsXG5cdFx0fSk7XG5cdFx0T2JqZWN0LmFzc2lnbih2aXJ0dWFsQmFyLnN0eWxlLCB7XG5cdFx0XHR3aWR0aDogYCR7eCh0b3RhbCl9cHhgLFxuXHRcdFx0aGVpZ2h0OiBcIjEwMCVcIixcblx0XHRcdGJvcmRlckNvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHRib3JkZXJXaWR0aDogXCIwcHggMXB4IDBweCAwcHhcIixcblx0XHRcdGJvcmRlclN0eWxlOiBcInNvbGlkXCIsXG5cdFx0XHRvcGFjaXR5OiAxLFxuXHRcdH0pO1xuXHRcdGxldCB2YmFycyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdFx0T2JqZWN0LmFzc2lnbih2YmFycy5zdHlsZSwge1xuXHRcdFx0d2lkdGg6IFwiMTAwJVwiLFxuXHRcdFx0aGVpZ2h0OiBcIjEwMCVcIixcblx0XHRcdGJhY2tncm91bmQ6XG5cdFx0XHRcdGByZXBlYXRpbmctbGluZWFyLWdyYWRpZW50KHRvIHJpZ2h0LCAke29wdHMuZmlsbENvbG9yfSAwcHgsICR7b3B0cy5maWxsQ29sb3J9IDFweCwgd2hpdGUgMXB4LCB3aGl0ZSAycHgpYCxcblx0XHR9KTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKHZiYXJzKTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKGhvdmVyQmFyKTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKHNlbGVjdEJhcik7XG5cdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KHZpcnR1YWxCYXIsIFwiZGF0YVwiLCB7XG5cdFx0XHR2YWx1ZTogc291cmNlLmJpbnMuc2xpY2UodGhyZXNoKSxcblx0XHR9KTtcblx0XHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gZGF0YSBpcyBkaWZmZXJlbnQgZm9yIHZpcnR1YWwgYmFyLi4uXG5cdFx0Ly8gVE9ETzogbmVlZCB0byByZXByZXNlbnQgZGlmZmVyZW5jZSBpbiB0eXBlc1xuXHRcdGJhcnMucHVzaCh2aXJ0dWFsQmFyKTtcblx0fVxuXG5cdGlmIChzb3VyY2UudW5pcXVlQ291bnQpIHtcblx0XHRsZXQgYmFyID0gY3JlYXRlQmFyKHtcblx0XHRcdHRpdGxlOiBcInVuaXF1ZVwiLFxuXHRcdFx0ZmlsbENvbG9yOiBvcHRzLmJhY2tncm91bmRCYXJDb2xvcixcblx0XHRcdHRleHRDb2xvcjogXCJ2YXIoLS1taWQtZ3JheSlcIixcblx0XHRcdHdpZHRoOiB4KHNvdXJjZS51bmlxdWVDb3VudCksXG5cdFx0XHRoZWlnaHQ6IG9wdHMuaGVpZ2h0LFxuXHRcdH0pO1xuXHRcdGJhci50aXRsZSA9IFwiX19xdWFrX3VuaXF1ZV9fXCI7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7XG5cdFx0XHRkYXRhOiB7XG5cdFx0XHRcdGtleTogXCJfX3F1YWtfdW5pcXVlX19cIixcblx0XHRcdFx0dG90YWw6IHNvdXJjZS51bmlxdWVDb3VudCxcblx0XHRcdH0sXG5cdFx0fSkpO1xuXHR9XG5cblx0aWYgKHNvdXJjZS5udWxsQ291bnQpIHtcblx0XHRsZXQgYmFyID0gY3JlYXRlQmFyKHtcblx0XHRcdHRpdGxlOiBcIm51bGxcIixcblx0XHRcdGZpbGxDb2xvcjogb3B0cy5udWxsRmlsbENvbG9yLFxuXHRcdFx0dGV4dENvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHR3aWR0aDogeChzb3VyY2UubnVsbENvdW50KSxcblx0XHRcdGhlaWdodDogb3B0cy5oZWlnaHQsXG5cdFx0fSk7XG5cdFx0YmFyLnRpdGxlID0gXCJfX3F1YWtfbnVsbF9fXCI7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7XG5cdFx0XHRkYXRhOiB7XG5cdFx0XHRcdGtleTogXCJfX3F1YWtfbnVsbF9fXCIsXG5cdFx0XHRcdHRvdGFsOiBzb3VyY2UudW5pcXVlQ291bnQsXG5cdFx0XHR9LFxuXHRcdH0pKTtcblx0fVxuXG5cdGxldCBmaXJzdCA9IGJhcnNbMF07XG5cdGxldCBsYXN0ID0gYmFyc1tiYXJzLmxlbmd0aCAtIDFdO1xuXHRpZiAoZmlyc3QgPT09IGxhc3QpIHtcblx0XHRmaXJzdC5zdHlsZS5ib3JkZXJSYWRpdXMgPSBcIjVweFwiO1xuXHR9IGVsc2Uge1xuXHRcdGZpcnN0LnN0eWxlLmJvcmRlclJhZGl1cyA9IFwiNXB4IDBweCAwcHggNXB4XCI7XG5cdFx0bGFzdC5zdHlsZS5ib3JkZXJSYWRpdXMgPSBcIjBweCA1cHggNXB4IDBweFwiO1xuXHR9XG5cblx0ZnVuY3Rpb24gdmlydHVhbEJpbihrZXk6IHN0cmluZykge1xuXHRcdGFzc2VydCh2aXJ0dWFsQmFyKTtcblx0XHQvL1RPRE86IElzIHRoZXJlIGEgYmV0dGVyIHdheSB0byBkbyB0aGlzP1xuXHRcdGxldCB2b2Zmc2V0ID0gYmFyc1xuXHRcdFx0LnNsaWNlKDAsIHRocmVzaClcblx0XHRcdC5tYXAoKGIpID0+IGIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkud2lkdGgpXG5cdFx0XHQucmVkdWNlKChhLCBiKSA9PiBhICsgYiwgMCk7XG5cblx0XHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gZGF0YSBpcyBhIHByb3BlcnR5IHdlIHNldCBvbiB0aGUgZWxlbWVudFxuXHRcdGxldCB2YmluczogQXJyYXk8eyBrZXk6IHN0cmluZzsgdG90YWw6IG51bWJlciB9PiA9IHZpcnR1YWxCYXIuZGF0YTtcblx0XHRsZXQgcmVjdCA9IHZpcnR1YWxCYXIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG5cdFx0bGV0IGR4ID0gcmVjdC53aWR0aCAvIHZiaW5zLmxlbmd0aDtcblx0XHRsZXQgaWR4ID0gdmJpbnMuZmluZEluZGV4KChkKSA9PiBkLmtleSA9PT0ga2V5KTtcblx0XHRhc3NlcnQoaWR4ICE9PSAtMSwgYGtleSAke2tleX0gbm90IGZvdW5kIGluIHZpcnR1YWwgYmluc2ApO1xuXHRcdHJldHVybiB7XG5cdFx0XHQuLi52Ymluc1tpZHhdLFxuXHRcdFx0eDogZHggKiBpZHggKyB2b2Zmc2V0LFxuXHRcdH07XG5cdH1cblxuXHRmdW5jdGlvbiByZXNldChvcGFjdGl5OiBudW1iZXIpIHtcblx0XHRiYXJzLmZvckVhY2goKGJhcikgPT4ge1xuXHRcdFx0aWYgKGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdmlydHVhbF9fXCIpIHtcblx0XHRcdFx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIHdlIHNldCB0aGlzIGFib3ZlXG5cdFx0XHRcdGxldCB2YmFyczogSFRNTERpdkVsZW1lbnQgPSBiYXIuZmlyc3RDaGlsZCE7XG5cdFx0XHRcdHZiYXJzLnN0eWxlLm9wYWNpdHkgPSBvcGFjdGl5LnRvU3RyaW5nKCk7XG5cdFx0XHRcdHZiYXJzLnN0eWxlLmJhY2tncm91bmQgPSBjcmVhdGVWaXJ0dWFsQmFyUmVwZWF0aW5nQmFja2dyb3VuZCh7XG5cdFx0XHRcdFx0Y29sb3I6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0XHR9KTtcblx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdGJhci5zdHlsZS5vcGFjaXR5ID0gb3BhY3RpeS50b1N0cmluZygpO1xuXHRcdFx0XHRiYXIuc3R5bGUuYmFja2dyb3VuZCA9IGNyZWF0ZVNwbGl0QmFyRmlsbCh7XG5cdFx0XHRcdFx0Y29sb3I6IGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIlxuXHRcdFx0XHRcdFx0PyBvcHRzLmJhY2tncm91bmRCYXJDb2xvclxuXHRcdFx0XHRcdFx0OiBiYXIudGl0bGUgPT09IFwiX19xdWFrX251bGxfX1wiXG5cdFx0XHRcdFx0XHQ/IG9wdHMubnVsbEZpbGxDb2xvclxuXHRcdFx0XHRcdFx0OiBvcHRzLmZpbGxDb2xvcixcblx0XHRcdFx0XHRiZ0NvbG9yOiBvcHRzLmJhY2tncm91bmRCYXJDb2xvcixcblx0XHRcdFx0XHRmcmFjOiAxLFxuXHRcdFx0XHR9KTtcblx0XHRcdH1cblx0XHRcdGJhci5zdHlsZS5ib3JkZXJDb2xvciA9IFwid2hpdGVcIjtcblx0XHRcdGJhci5zdHlsZS5ib3JkZXJXaWR0aCA9IFwiMHB4IDFweCAwcHggMHB4XCI7XG5cdFx0XHRiYXIuc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJib3gtc2hhZG93XCIpO1xuXHRcdH0pO1xuXHRcdGJhcnNbYmFycy5sZW5ndGggLSAxXS5zdHlsZS5ib3JkZXJXaWR0aCA9IFwiMHB4XCI7XG5cdFx0aG92ZXJCYXIuc3R5bGUudmlzaWJpbGl0eSA9IFwiaGlkZGVuXCI7XG5cdFx0c2VsZWN0QmFyLnN0eWxlLnZpc2liaWxpdHkgPSBcImhpZGRlblwiO1xuXHR9XG5cblx0ZnVuY3Rpb24gaG92ZXIoa2V5OiBzdHJpbmcsIHNlbGVjdGVkPzogc3RyaW5nKSB7XG5cdFx0bGV0IGJhciA9IGJhcnMuZmluZCgoYikgPT4gYi5kYXRhLmtleSA9PT0ga2V5KTtcblx0XHRpZiAoYmFyICE9PSB1bmRlZmluZWQpIHtcblx0XHRcdGJhci5zdHlsZS5vcGFjaXR5ID0gXCIxXCI7XG5cdFx0XHRyZXR1cm47XG5cdFx0fVxuXHRcdGxldCB2YmluID0gdmlydHVhbEJpbihrZXkpO1xuXHRcdGhvdmVyQmFyLnRpdGxlID0gdmJpbi5rZXk7XG5cdFx0aG92ZXJCYXIuZGF0YSA9IHZiaW47XG5cdFx0aG92ZXJCYXIuc3R5bGUub3BhY2l0eSA9IHNlbGVjdGVkID8gXCIwLjI1XCIgOiBcIjFcIjtcblx0XHRob3ZlckJhci5zdHlsZS5sZWZ0ID0gYCR7dmJpbi54fXB4YDtcblx0XHRob3ZlckJhci5zdHlsZS52aXNpYmlsaXR5ID0gXCJ2aXNpYmxlXCI7XG5cdH1cblxuXHRmdW5jdGlvbiBzZWxlY3Qoa2V5OiBzdHJpbmcpIHtcblx0XHRsZXQgYmFyID0gYmFycy5maW5kKChiKSA9PiBiLmRhdGEua2V5ID09PSBrZXkpO1xuXHRcdGlmIChiYXIgIT09IHVuZGVmaW5lZCkge1xuXHRcdFx0YmFyLnN0eWxlLm9wYWNpdHkgPSBcIjFcIjtcblx0XHRcdGJhci5zdHlsZS5ib3hTaGFkb3cgPSBcImluc2V0IDAgMCAwIDEuMnB4IGJsYWNrXCI7XG5cdFx0XHRyZXR1cm47XG5cdFx0fVxuXHRcdGxldCB2YmluID0gdmlydHVhbEJpbihrZXkpO1xuXHRcdHNlbGVjdEJhci5zdHlsZS5vcGFjaXR5ID0gXCIxXCI7XG5cdFx0c2VsZWN0QmFyLnRpdGxlID0gdmJpbi5rZXk7XG5cdFx0c2VsZWN0QmFyLmRhdGEgPSB2YmluO1xuXHRcdHNlbGVjdEJhci5zdHlsZS5sZWZ0ID0gYCR7dmJpbi54fXB4YDtcblx0XHRzZWxlY3RCYXIuc3R5bGUudmlzaWJpbGl0eSA9IFwidmlzaWJsZVwiO1xuXHR9XG5cblx0bGV0IGNvdW50czogUmVjb3JkPHN0cmluZywgbnVtYmVyPiA9IE9iamVjdC5mcm9tRW50cmllcyhcblx0XHRBcnJheS5mcm9tKGRhdGEudG9BcnJheSgpLCAoZCkgPT4gW2Qua2V5LCBkLnRvdGFsXSksXG5cdCk7XG5cblx0cmV0dXJuIHtcblx0XHRlbGVtZW50czogYmFycyxcblx0XHRuZWFyZXN0WChldmVudDogTW91c2VFdmVudCk6IHN0cmluZyB8IHVuZGVmaW5lZCB7XG5cdFx0XHRsZXQgYmFyID0gbmVhcmVzdFgoZXZlbnQsIGJhcnMpO1xuXHRcdFx0aWYgKCFiYXIpIHJldHVybjtcblx0XHRcdGlmIChiYXIudGl0bGUgIT09IFwiX19xdWFrX3ZpcnR1YWxfX1wiKSB7XG5cdFx0XHRcdC8vIEB0cy1leHBlY3QtZXJyb3IgLSBkYXRhIGlzIGEgcHJvcGVydHkgd2Ugc2V0IG9uIHRoZSBlbGVtZW50XG5cdFx0XHRcdHJldHVybiBiYXIuZGF0YS5rZXk7XG5cdFx0XHR9XG5cdFx0XHRsZXQgcmVjdCA9IGJhci5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcblx0XHRcdGxldCBtb3VzZVggPSBldmVudC5jbGllbnRYIC0gcmVjdC5sZWZ0O1xuXHRcdFx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIGRhdGEgaXMgYSBwcm9wZXJ0eSB3ZSBzZXQgb24gdGhlIGVsZW1lbnRcblx0XHRcdGxldCBkYXRhOiBBcnJheTx7IGtleTogc3RyaW5nOyB0b3RhbDogbnVtYmVyIH0+ID0gYmFyLmRhdGE7XG5cdFx0XHRsZXQgaWR4ID0gTWF0aC5mbG9vcigobW91c2VYIC8gcmVjdC53aWR0aCkgKiBkYXRhLmxlbmd0aCk7XG5cdFx0XHRyZXR1cm4gZGF0YVtpZHhdLmtleTtcblx0XHR9LFxuXHRcdHJlbmRlcihkYXRhOiBDb3VudFRhYmxlRGF0YSwgaG92ZXJpbmc/OiBzdHJpbmcsIHNlbGVjdGVkPzogc3RyaW5nKSB7XG5cdFx0XHRyZXNldChob3ZlcmluZyB8fCBzZWxlY3RlZCA/IDAuNCA6IDEpO1xuXHRcdFx0bGV0IHVwZGF0ZTogUmVjb3JkPHN0cmluZywgbnVtYmVyPiA9IE9iamVjdC5mcm9tRW50cmllcyhcblx0XHRcdFx0QXJyYXkuZnJvbShkYXRhLnRvQXJyYXkoKSwgKGQpID0+IFtkLmtleSwgZC50b3RhbF0pLFxuXHRcdFx0KTtcblx0XHRcdGxldCB0b3RhbCA9IE9iamVjdC52YWx1ZXModXBkYXRlKS5yZWR1Y2UoKGEsIGIpID0+IGEgKyBiLCAwKTtcblx0XHRcdGZvciAobGV0IGJhciBvZiBiYXJzKSB7XG5cdFx0XHRcdGlmIChiYXIudGl0bGUgPT09IFwiX19xdWFrX3ZpcnR1YWxfX1wiKSB7XG5cdFx0XHRcdFx0bGV0IHZiYXJzID0gYmFyLmZpcnN0Q2hpbGQgYXMgSFRNTERpdkVsZW1lbnQ7XG5cdFx0XHRcdFx0dmJhcnMuc3R5bGUuYmFja2dyb3VuZCA9IGNyZWF0ZVZpcnR1YWxCYXJSZXBlYXRpbmdCYWNrZ3JvdW5kKHtcblx0XHRcdFx0XHRcdGNvbG9yOiAodG90YWwgPCBzb3VyY2UudG90YWwpIHx8IHNlbGVjdGVkXG5cdFx0XHRcdFx0XHRcdD8gb3B0cy5iYWNrZ3JvdW5kQmFyQ29sb3Jcblx0XHRcdFx0XHRcdFx0OiBvcHRzLmZpbGxDb2xvcixcblx0XHRcdFx0XHR9KTtcblx0XHRcdFx0fSBlbHNlIHtcblx0XHRcdFx0XHRsZXQga2V5OiBzdHJpbmcgPSBiYXIuZGF0YS5rZXk7XG5cdFx0XHRcdFx0bGV0IGZyYWMgPSAodXBkYXRlW2tleV0gPz8gMCkgLyBjb3VudHNba2V5XTtcblx0XHRcdFx0XHRpZiAoc2VsZWN0ZWQpIGZyYWMgPSBrZXkgPT09IHNlbGVjdGVkID8gZnJhYyA6IDA7XG5cdFx0XHRcdFx0YmFyLnN0eWxlLmJhY2tncm91bmQgPSBjcmVhdGVTcGxpdEJhckZpbGwoe1xuXHRcdFx0XHRcdFx0Y29sb3I6IGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIlxuXHRcdFx0XHRcdFx0XHQ/IG9wdHMuYmFja2dyb3VuZEJhckNvbG9yXG5cdFx0XHRcdFx0XHRcdDogYmFyLnRpdGxlID09PSBcIl9fcXVha19udWxsX19cIlxuXHRcdFx0XHRcdFx0XHQ/IG9wdHMubnVsbEZpbGxDb2xvclxuXHRcdFx0XHRcdFx0XHQ6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0XHRcdFx0YmdDb2xvcjogb3B0cy5iYWNrZ3JvdW5kQmFyQ29sb3IsXG5cdFx0XHRcdFx0XHRmcmFjOiBpc05hTihmcmFjKSA/IDAgOiBmcmFjLFxuXHRcdFx0XHRcdH0pO1xuXHRcdFx0XHR9XG5cdFx0XHR9XG5cdFx0XHRpZiAoaG92ZXJpbmcgIT09IHVuZGVmaW5lZCkge1xuXHRcdFx0XHRob3Zlcihob3ZlcmluZywgc2VsZWN0ZWQpO1xuXHRcdFx0fVxuXHRcdFx0aWYgKHNlbGVjdGVkICE9PSB1bmRlZmluZWQpIHtcblx0XHRcdFx0c2VsZWN0KHNlbGVjdGVkKTtcblx0XHRcdH1cblx0XHR9LFxuXHRcdHRleHRGb3Ioa2V5Pzogc3RyaW5nKTogc3RyaW5nIHtcblx0XHRcdGlmIChrZXkgPT09IHVuZGVmaW5lZCkge1xuXHRcdFx0XHRsZXQgbmNhdHMgPSBkYXRhLm51bVJvd3M7XG5cdFx0XHRcdHJldHVybiBgJHtuY2F0cy50b0xvY2FsZVN0cmluZygpfSBjYXRlZ29yJHtuY2F0cyA9PT0gMSA/IFwieVwiIDogXCJpZXNcIn1gO1xuXHRcdFx0fVxuXHRcdFx0aWYgKGtleSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIikge1xuXHRcdFx0XHRyZXR1cm4gYCR7c291cmNlLnVuaXF1ZUNvdW50LnRvTG9jYWxlU3RyaW5nKCl9IHVuaXF1ZSB2YWx1ZSR7XG5cdFx0XHRcdFx0c291cmNlLnVuaXF1ZUNvdW50ID09PSAxID8gXCJcIiA6IFwic1wiXG5cdFx0XHRcdH1gO1xuXHRcdFx0fVxuXHRcdFx0aWYgKGtleSA9PT0gXCJfX3F1YWtfbnVsbF9fXCIpIHtcblx0XHRcdFx0cmV0dXJuIFwibnVsbFwiO1xuXHRcdFx0fVxuXHRcdFx0cmV0dXJuIGtleS50b1N0cmluZygpO1xuXHRcdH0sXG5cdH07XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZVRleHRPdXRwdXQoKSB7XG5cdGxldCBub2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0T2JqZWN0LmFzc2lnbihub2RlLnN0eWxlLCB7XG5cdFx0cG9pbnRlckV2ZW50czogXCJub25lXCIsXG5cdFx0aGVpZ2h0OiBcIjE1cHhcIixcblx0XHRtYXhXaWR0aDogXCIxMDAlXCIsXG5cdFx0b3ZlcmZsb3c6IFwiaGlkZGVuXCIsXG5cdFx0dGV4dE92ZXJmbG93OiBcImVsbGlwc2lzXCIsXG5cdFx0cG9zaXRpb246IFwiYWJzb2x1dGVcIixcblx0XHRmb250V2VpZ2h0OiA0MDAsXG5cdFx0bWFyZ2luVG9wOiBcIjEuNXB4XCIsXG5cdFx0Y29sb3I6IFwidmFyKC0tbWlkLWdyYXkpXCIsXG5cdH0pO1xuXHRyZXR1cm4gbm9kZTtcbn1cblxuZnVuY3Rpb24gY3JlYXRlVmlydHVhbFNlbGVjdGlvbkJhcihvcHRzOiB7IGZpbGxDb2xvcjogc3RyaW5nIH0pIHtcblx0bGV0IG5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuXHRPYmplY3QuYXNzaWduKG5vZGUuc3R5bGUsIHtcblx0XHRwb3NpdGlvbjogXCJhYnNvbHV0ZVwiLFxuXHRcdHRvcDogXCIwXCIsXG5cdFx0d2lkdGg6IFwiMS41cHhcIixcblx0XHRoZWlnaHQ6IFwiMTAwJVwiLFxuXHRcdGJhY2tncm91bmRDb2xvcjogb3B0cy5maWxsQ29sb3IsXG5cdFx0cG9pbnRlckV2ZW50czogXCJub25lXCIsXG5cdFx0dmlzaWJpbGl0eTogXCJoaWRkZW5cIixcblx0fSk7XG5cdHJldHVybiBPYmplY3QuYXNzaWduKG5vZGUsIHtcblx0XHRkYXRhOiB7IGtleTogXCJcIiwgdG90YWw6IDAgfSxcblx0fSk7XG59XG5cbmZ1bmN0aW9uIG5lYXJlc3RYKHsgY2xpZW50WCB9OiBNb3VzZUV2ZW50LCBiYXJzOiBBcnJheTxIVE1MRWxlbWVudD4pIHtcblx0Ly8gY291bGQgdXNlIGEgYmluYXJ5IHNlYXJjaCBoZXJlIGlmIG5lZWRlZFxuXHRmb3IgKGxldCBiYXIgb2YgYmFycykge1xuXHRcdGxldCByZWN0ID0gYmFyLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuXHRcdGlmIChjbGllbnRYID49IHJlY3QubGVmdCAmJiBjbGllbnRYIDw9IHJlY3QucmlnaHQpIHtcblx0XHRcdHJldHVybiBiYXI7XG5cdFx0fVxuXHR9XG59XG5cbi8qKlxuICogQ3JlYXRlcyBhIGZpbGwgZ3JhZGllbnQgdGhhdCBpcyBmaWxsZWQgeCUgd2l0aCBhIGNvbG9yIGFuZCB0aGUgcmVzdCB3aXRoIGEgYmFja2dyb3VuZCBjb2xvci5cbiAqL1xuZnVuY3Rpb24gY3JlYXRlU3BsaXRCYXJGaWxsKFxuXHRvcHRpb25zOiB7IGNvbG9yOiBzdHJpbmc7IGJnQ29sb3I6IHN0cmluZzsgZnJhYzogbnVtYmVyIH0sXG4pIHtcblx0bGV0IHsgY29sb3IsIGJnQ29sb3IsIGZyYWMgfSA9IG9wdGlvbnM7XG5cdGxldCBwID0gZnJhYyAqIDEwMDtcblx0Ly8gZGVuby1mbXQtaWdub3JlXG5cdHJldHVybiBgbGluZWFyLWdyYWRpZW50KHRvIHRvcCwgJHtjb2xvcn0gJHtwfSUsICR7YmdDb2xvcn0gJHtwfSUsICR7YmdDb2xvcn0gJHsxMDAgLSBwfSUpYDtcbn1cblxuZnVuY3Rpb24gY3JlYXRlVmlydHVhbEJhclJlcGVhdGluZ0JhY2tncm91bmQoeyBjb2xvciB9OiB7IGNvbG9yOiBzdHJpbmcgfSkge1xuXHRyZXR1cm4gYHJlcGVhdGluZy1saW5lYXItZ3JhZGllbnQodG8gcmlnaHQsICR7Y29sb3J9IDBweCwgJHtjb2xvcn0gMXB4LCB3aGl0ZSAxcHgsIHdoaXRlIDJweClgO1xufVxuIiwgIjpob3N0IHtcblx0YWxsOiBpbml0aWFsO1xuXHQtLXNhbnMtc2VyaWY6IC1hcHBsZS1zeXN0ZW0sIEJsaW5rTWFjU3lzdGVtRm9udCwgXCJhdmVuaXIgbmV4dFwiLCBhdmVuaXIsIGhlbHZldGljYSwgXCJoZWx2ZXRpY2EgbmV1ZVwiLCB1YnVudHUsIHJvYm90bywgbm90bywgXCJzZWdvZSB1aVwiLCBhcmlhbCwgc2Fucy1zZXJpZjtcblx0LS1saWdodC1zaWx2ZXI6ICNlZmVmZWY7XG5cdC0tc3BhY2luZy1ub25lOiAwO1xuXHQtLXdoaXRlOiAjZmZmO1xuXHQtLWdyYXk6ICM5MjkyOTI7XG5cdC0tZGFyay1ncmF5OiAjMzMzO1xuXHQtLW1vb24tZ3JheTogI2M0YzRjNDtcblx0LS1taWQtZ3JheTogIzZlNmU2ZTtcblxuXHQtLXN0b25lLWJsdWU6ICM2NDc0OGI7XG5cdC0teWVsbG93LWdvbGQ6ICNjYThhMDQ7XG5cblx0LS10ZWFsOiAjMDI3OTgyO1xuXHQtLWRhcmstcGluazogI0QzNUE1RjtcblxuXHQtLWxpZ2h0LWJsdWU6ICM3RTkzQ0Y7XG5cdC0tZGFyay15ZWxsb3ctZ29sZDogI0E5ODQ0NztcblxuXHQtLXB1cnBsZTogIzk4N2ZkMztcblxuXHQtLXByaW1hcnk6IHZhcigtLXN0b25lLWJsdWUpO1xuXHQtLXNlY29uZGFyeTogdmFyKC0teWVsbG93LWdvbGQpO1xufVxuXG4uaGlnaGxpZ2h0IHtcblx0YmFja2dyb3VuZC1jb2xvcjogdmFyKC0tbGlnaHQtc2lsdmVyKTtcbn1cblxuLmhpZ2hsaWdodC1jZWxsIHtcblx0Ym9yZGVyOiAxcHggc29saWQgdmFyKC0tbW9vbi1ncmF5KTtcbn1cblxuLnF1YWsge1xuICBib3JkZXItcmFkaXVzOiAwLjJyZW07XG4gIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWxpZ2h0LXNpbHZlcik7XG4gIG92ZXJmbG93LXk6IGF1dG87XG59XG5cbnRhYmxlIHtcbiAgYm9yZGVyLWNvbGxhcHNlOiBzZXBhcmF0ZTtcbiAgYm9yZGVyLXNwYWNpbmc6IDA7XG4gIHdoaXRlLXNwYWNlOiBub3dyYXA7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG5cbiAgbWFyZ2luOiB2YXIoLS1zcGFjaW5nLW5vbmUpO1xuICBjb2xvcjogdmFyKC0tZGFyay1ncmF5KTtcbiAgZm9udDogMTNweCAvIDEuMiB2YXIoLS1zYW5zLXNlcmlmKTtcblxuICB3aWR0aDogMTAwJTtcbn1cblxudGhlYWQge1xuICBwb3NpdGlvbjogc3RpY2t5O1xuICB2ZXJ0aWNhbC1hbGlnbjogdG9wO1xuICB0ZXh0LWFsaWduOiBsZWZ0O1xuICB0b3A6IDA7XG59XG5cbnRkIHtcbiAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tbGlnaHQtc2lsdmVyKTtcbiAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHRyYW5zcGFyZW50O1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB0cmFuc3BhcmVudDtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgLW8tdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XG4gIHRleHQtb3ZlcmZsb3c6IGVsbGlwc2lzO1xuICBwYWRkaW5nOiA0cHggNnB4O1xufVxuXG50cjpmaXJzdC1jaGlsZCB0ZCB7XG4gIGJvcmRlci10b3A6IHNvbGlkIDFweCB0cmFuc3BhcmVudDtcbn1cblxudGgge1xuICBkaXNwbGF5OiB0YWJsZS1jZWxsO1xuICB2ZXJ0aWNhbC1hbGlnbjogaW5oZXJpdDtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHRleHQtYWxpZ246IC1pbnRlcm5hbC1jZW50ZXI7XG4gIHVuaWNvZGUtYmlkaTogaXNvbGF0ZTtcblxuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIGJhY2tncm91bmQ6IHZhcigtLXdoaXRlKTtcbiAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHZhcigtLWxpZ2h0LXNpbHZlcik7XG4gIGJvcmRlci1sZWZ0OiBzb2xpZCAxcHggdmFyKC0tbGlnaHQtc2lsdmVyKTtcbiAgcGFkZGluZzogNXB4IDZweDtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG59XG5cbi5udW1iZXIsIC5kYXRlIHtcbiAgZm9udC12YXJpYW50LW51bWVyaWM6IHRhYnVsYXItbnVtcztcbn1cblxuLmdyYXkge1xuICBjb2xvcjogdmFyKC0tZ3JheSk7XG59XG5cbi5udW1iZXIge1xuICB0ZXh0LWFsaWduOiByaWdodDtcbn1cblxudGQ6bnRoLWNoaWxkKDEpLCB0aDpudGgtY2hpbGQoMSkge1xuICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGNvbG9yOiB2YXIoLS1tb29uLWdyYXkpO1xuICBwYWRkaW5nOiAwIDRweDtcbn1cblxudGQ6Zmlyc3QtY2hpbGQsIHRoOmZpcnN0LWNoaWxkIHtcbiAgYm9yZGVyLWxlZnQ6IG5vbmU7XG59XG5cbnRoOmZpcnN0LWNoaWxkIHtcbiAgYm9yZGVyLWxlZnQ6IG5vbmU7XG4gIHZlcnRpY2FsLWFsaWduOiB0b3A7XG4gIHdpZHRoOiAyMHB4O1xuICBwYWRkaW5nOiA3cHg7XG59XG5cbnRkOm50aC1sYXN0LWNoaWxkKDIpLCB0aDpudGgtbGFzdC1jaGlsZCgyKSB7XG4gIGJvcmRlci1yaWdodDogMXB4IHNvbGlkIHZhcigtLWxpZ2h0LXNpbHZlcik7XG59XG5cbnRyOmZpcnN0LWNoaWxkIHRkIHtcblx0Ym9yZGVyLXRvcDogc29saWQgMXB4IHRyYW5zcGFyZW50O1xufVxuXG4ucmVzaXplLWhhbmRsZSB7XG5cdHdpZHRoOiA1cHg7XG5cdGhlaWdodDogMTAwJTtcblx0YmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcblx0cmlnaHQ6IC0yLjVweDtcblx0dG9wOiAwO1xuXHRjdXJzb3I6IGV3LXJlc2l6ZTtcblx0ei1pbmRleDogMTtcbn1cblxuLnF1YWsgLnNvcnQtYnV0dG9uIHtcblx0Y3Vyc29yOiBwb2ludGVyO1xuXHRiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS13aGl0ZSk7XG5cdHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4uc3RhdHVzLWJhciB7XG5cdGRpc3BsYXk6IGZsZXg7XG5cdGp1c3RpZnktY29udGVudDogZmxleC1lbmQ7XG5cdGZvbnQtZmFtaWx5OiB2YXIoLS1zYW5zLXNlcmlmKTtcblx0bWFyZ2luLXJpZ2h0OiAxMHB4O1xuXHRtYXJnaW4tdG9wOiA1cHg7XG59XG5cbi5zdGF0dXMtYmFyIGJ1dHRvbiB7XG5cdGJvcmRlcjogbm9uZTtcblx0YmFja2dyb3VuZC1jb2xvcjogdmFyKC0td2hpdGUpO1xuXHRjb2xvcjogdmFyKC0tcHJpbWFyeSk7XG5cdGZvbnQtd2VpZ2h0OiA2MDA7XG5cdGZvbnQtc2l6ZTogMC44NzVyZW07XG5cdGN1cnNvcjogcG9pbnRlcjtcblx0bWFyZ2luLXJpZ2h0OiA1cHg7XG59XG5cbi5zdGF0dXMtYmFyIHNwYW4ge1xuXHRjb2xvcjogdmFyKC0tZ3JheSk7XG5cdGZvbnQtd2VpZ2h0OiA0MDA7XG5cdGZvbnQtc2l6ZTogMC43NXJlbTtcblx0Zm9udC12YXJpYW50LW51bWVyaWM6IHRhYnVsYXItbnVtcztcbn1cbiIsICJpbXBvcnQgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG4vLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLWNvcmUuZC50c1wiXG5pbXBvcnQgeyB0eXBlIEludGVyYWN0b3IsIE1vc2FpY0NsaWVudCwgU2VsZWN0aW9uIH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLWNvcmVcIjtcbi8vIEBkZW5vLXR5cGVzPVwiLi4vZGVwcy9tb3NhaWMtc3FsLmQudHNcIlxuaW1wb3J0IHsgY291bnQsIFF1ZXJ5IH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuXG5pbnRlcmZhY2UgU3RhdHVzQmFyT3B0aW9ucyB7XG5cdHRhYmxlOiBzdHJpbmc7XG5cdGZpbHRlckJ5PzogU2VsZWN0aW9uO1xufVxuXG5leHBvcnQgY2xhc3MgU3RhdHVzQmFyIGV4dGVuZHMgTW9zYWljQ2xpZW50IHtcblx0I3RhYmxlOiBzdHJpbmc7XG5cdCNlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdCNidXR0b246IEhUTUxCdXR0b25FbGVtZW50O1xuXHQjc3BhbjogSFRNTFNwYW5FbGVtZW50O1xuXHQjdG90YWxSb3dzOiBudW1iZXIgfCB1bmRlZmluZWQgPSB1bmRlZmluZWQ7XG5cblx0Y29uc3RydWN0b3Iob3B0aW9uczogU3RhdHVzQmFyT3B0aW9ucykge1xuXHRcdHN1cGVyKG9wdGlvbnMuZmlsdGVyQnkpO1xuXHRcdHRoaXMuI3RhYmxlID0gb3B0aW9ucy50YWJsZTtcblx0XHR0aGlzLiNidXR0b24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIpO1xuXHRcdHRoaXMuI2J1dHRvbi5pbm5lclRleHQgPSBcIlJlc2V0XCI7XG5cdFx0dGhpcy4jc3BhbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJzcGFuXCIpO1xuXG5cdFx0bGV0IGRpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdFx0ZGl2LmFwcGVuZENoaWxkKHRoaXMuI2J1dHRvbik7XG5cdFx0ZGl2LmFwcGVuZENoaWxkKHRoaXMuI3NwYW4pO1xuXHRcdHRoaXMuI2VsLmFwcGVuZENoaWxkKGRpdik7XG5cdFx0dGhpcy4jZWwuY2xhc3NMaXN0LmFkZChcInN0YXR1cy1iYXJcIik7XG5cblx0XHR0aGlzLiNidXR0b24uYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlZG93blwiLCAoKSA9PiB7XG5cdFx0XHRpZiAoIXRoaXMuZmlsdGVyQnkpIHJldHVybjtcblx0XHRcdC8vIFRPRE86IEEgYmV0dGVyIHdheSB0byBkbyB0aGlzP1xuXHRcdFx0Ly8gV2Ugd2FudCB0byBjbGVhciBhbGwgdGhlIGV4aXN0aW5nIHNlbGVjdGlvbnNcblx0XHRcdC8vIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3V3ZGF0YS9tb3NhaWMvYmxvYi84ZTYzMTQ5NzUzZTdkNmNhMzAyNzRjMDMyYTA0NzQ0ZTE0ZGYyZmQ2L3BhY2thZ2VzL2NvcmUvc3JjL1NlbGVjdGlvbi5qcyNMMjY1LUwyNzJcblx0XHRcdGZvciAobGV0IHsgc291cmNlIH0gb2YgdGhpcy5maWx0ZXJCeS5jbGF1c2VzKSB7XG5cdFx0XHRcdGlmICghaXNJbnRlcmFjdG9yKHNvdXJjZSkpIHtcblx0XHRcdFx0XHRjb25zb2xlLndhcm4oXCJTa2lwcGluZyBub24taW50ZXJhY3RvciBzb3VyY2VcIiwgc291cmNlKTtcblx0XHRcdFx0XHRjb250aW51ZTtcblx0XHRcdFx0fVxuXHRcdFx0XHRzb3VyY2UucmVzZXQoKTtcblx0XHRcdFx0dGhpcy5maWx0ZXJCeS51cGRhdGUoc291cmNlLmNsYXVzZSgpKTtcblx0XHRcdH1cblx0XHR9KTtcblxuXHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJoaWRkZW5cIjtcblx0XHR0aGlzLmZpbHRlckJ5Py5hZGRFdmVudExpc3RlbmVyKFwidmFsdWVcIiwgKCkgPT4ge1xuXHRcdFx0Ly8gZGVjaWRlIHdoZXRoZXIgdG8gZGlzcGxheSB0aGUgcmVzZXQgYnV0dG9uIGFueSB0aW1lIHRoZSBmaWx0ZXIgY2hhbmdlc1xuXHRcdFx0aWYgKHRoaXMuZmlsdGVyQnk/LmNsYXVzZXMubGVuZ3RoID09PSAwKSB7XG5cdFx0XHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJoaWRkZW5cIjtcblx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJ2aXNpYmxlXCI7XG5cdFx0XHR9XG5cdFx0fSk7XG5cdH1cblxuXHRxdWVyeShmaWx0ZXIgPSBbXSkge1xuXHRcdGxldCBxdWVyeSA9IFF1ZXJ5LmZyb20odGhpcy4jdGFibGUpXG5cdFx0XHQuc2VsZWN0KHsgY291bnQ6IGNvdW50KCkgfSlcblx0XHRcdC53aGVyZShmaWx0ZXIpO1xuXHRcdHJldHVybiBxdWVyeTtcblx0fVxuXG5cdHF1ZXJ5UmVzdWx0KHRhYmxlOiBhcnJvdy5UYWJsZTx7IGNvdW50OiBhcnJvdy5JbnQgfT4pIHtcblx0XHRsZXQgY291bnQgPSBOdW1iZXIodGFibGUuZ2V0KDApPy5jb3VudCA/PyAwKTtcblx0XHRpZiAoIXRoaXMuI3RvdGFsUm93cykge1xuXHRcdFx0Ly8gd2UgbmVlZCB0byBrbm93IHRoZSB0b3RhbCBudW1iZXIgb2Ygcm93cyB0byBkaXNwbGF5XG5cdFx0XHR0aGlzLiN0b3RhbFJvd3MgPSBjb3VudDtcblx0XHR9XG5cdFx0bGV0IGNvdW50U3RyID0gY291bnQudG9Mb2NhbGVTdHJpbmcoKTtcblx0XHRpZiAoY291bnQgPT0gdGhpcy4jdG90YWxSb3dzKSB7XG5cdFx0XHR0aGlzLiNzcGFuLmlubmVyVGV4dCA9IGAke2NvdW50U3RyfSByb3dzYDtcblx0XHR9IGVsc2Uge1xuXHRcdFx0bGV0IHRvdGFsU3RyID0gdGhpcy4jdG90YWxSb3dzLnRvTG9jYWxlU3RyaW5nKCk7XG5cdFx0XHR0aGlzLiNzcGFuLmlubmVyVGV4dCA9IGAke2NvdW50U3RyfSBvZiAke3RvdGFsU3RyfSByb3dzYDtcblx0XHR9XG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHRub2RlKCkge1xuXHRcdHJldHVybiB0aGlzLiNlbDtcblx0fVxufVxuXG5mdW5jdGlvbiBpc09iamVjdCh4OiB1bmtub3duKTogeCBpcyBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPiB7XG5cdHJldHVybiB0eXBlb2YgeCA9PT0gXCJvYmplY3RcIiAmJiB4ICE9PSBudWxsICYmICFBcnJheS5pc0FycmF5KHgpO1xufVxuXG5mdW5jdGlvbiBpc0ludGVyYWN0b3IoeDogdW5rbm93bik6IHggaXMgSW50ZXJhY3RvciB7XG5cdHJldHVybiBpc09iamVjdCh4KSAmJiBcImNsYXVzZVwiIGluIHggJiYgXCJyZXNldFwiIGluIHg7XG59XG4iLCAiLyoqXG4gKiBEZWZlciBhIHByb21pc2UuXG4gKlxuICogVE9ETzogU2hvdWxkIHVzZSBQcm9taXNlLndpdGhSZXNvbHZlcnMoKSB3aGVuIGF2YWlsYWJsZS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGRlZmVyPFN1Y2Nlc3MsIFJlamVjdD4oKToge1xuXHRwcm9taXNlOiBQcm9taXNlPFN1Y2Nlc3M+O1xuXHRyZXNvbHZlOiAodmFsdWU6IFN1Y2Nlc3MpID0+IHZvaWQ7XG5cdHJlamVjdDogKHJlYXNvbj86IFJlamVjdCkgPT4gdm9pZDtcbn0ge1xuXHRsZXQgcmVzb2x2ZTtcblx0bGV0IHJlamVjdDtcblx0bGV0IHByb21pc2UgPSBuZXcgUHJvbWlzZTxTdWNjZXNzPigocmVzLCByZWopID0+IHtcblx0XHRyZXNvbHZlID0gcmVzO1xuXHRcdHJlamVjdCA9IHJlajtcblx0fSk7XG5cdC8qKiBAdHMtZXhwZWN0LWVycm9yIC0gcmVzb2x2ZSBhbmQgcmVqZWN0IGFyZSBzZXQgKi9cblx0cmV0dXJuIHsgcHJvbWlzZSwgcmVzb2x2ZSwgcmVqZWN0IH07XG59XG4iXSwKICAibWFwcGluZ3MiOiAiOzs7Ozs7Ozs7Ozs7Ozs7QUFDQSxZQUFZLFFBQVE7QUFFcEIsU0FBUyxTQUFBQSxjQUFhO0FBQ3RCLFlBQVlDLFlBQVc7QUFDdkIsWUFBWSxVQUFVO0FBRXRCLFNBQVMsVUFBQUMsZUFBYzs7O0FDUHZCLFlBQVlDLFlBQVc7QUFFdkI7QUFBQSxFQUlDLGdCQUFBQztBQUFBLEVBQ0EsYUFBQUM7QUFBQSxPQUNNO0FBRVAsU0FBUyxNQUFNLFNBQUFDLGNBQTRCO0FBQzNDLFlBQVksYUFBYTtBQUN6QixTQUFTLFlBQVk7OztBQ1RkLElBQU0saUJBQU4s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QUssTUFBTSxJQUFJLGFBQWEsQ0FBQyxFQUM3QixPQUFPLEdBQUcsTUFBTSxJQUFJLFVBQVUsQ0FBQyxFQUMvQixNQUFNLENBQUMsRUFDUCxTQUFTO0FBQUEsTUFDWjtBQUNBLGVBQVMsTUFBTTtBQUVmLGFBQU8sTUFBTTtBQUNaLG9CQUFZLE1BQU07QUFBQSxNQUNuQjtBQUFBLElBQ0Q7QUFBQSxJQUNBLE9BQU8sRUFBRSxPQUFPLEdBQUcsR0FBMEI7QUFDNUMsVUFBSSxRQUFRLElBQUksVUFBVTtBQUFBLFFBQ3pCLE9BQU8sTUFBTSxJQUFJLGFBQWE7QUFBQSxRQUM5QjtBQUFBLE1BQ0QsQ0FBQztBQUNELGtCQUFZLFFBQVEsS0FBSztBQUN6QixNQUFBQyxRQUFPLE1BQU07QUFDWixjQUFNLElBQUksT0FBTyxNQUFNLE9BQU8sRUFBRTtBQUNoQyxjQUFNLGFBQWE7QUFBQSxNQUNwQixDQUFDO0FBQ0QsU0FBRyxZQUFZLE1BQU0sS0FBSyxDQUFDO0FBQUEsSUFDNUI7QUFBQSxFQUNEO0FBQ0Q7QUFFQSxTQUFTLGNBQWM7QUFDdEIsU0FBTyxPQUFPO0FBQUEsSUFDYixPQUFPLEtBQUssT0FBTyxFQUFFLElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxNQUFNO0FBQUEsSUFBQyxDQUFDLENBQUM7QUFBQSxFQUNsRDtBQUNEOyIsCiAgIm5hbWVzIjogWyJRdWVyeSIsICJhcnJvdyIsICJlZmZlY3QiLCAiYXJyb3ciLCAiTW9zYWljQ2xpZW50IiwgIlNlbGVjdGlvbiIsICJRdWVyeSIsICJmb3JtYXQiLCAiZm10IiwgImJpbnMiLCAibnVsbENvdW50IiwgInR5cGUiLCAiYmluIiwgIk1vc2FpY0NsaWVudCIsICJjb3VudCIsICJRdWVyeSIsICJlZmZlY3QiLCAiZWZmZWN0IiwgInNpZ25hbCIsICJzaWduYWwiLCAiZWZmZWN0IiwgInNlbGVjdCIsICJkYXRhIiwgIk1vc2FpY0NsaWVudCIsICJRdWVyeSIsICJjb3VudCIsICJlZmZlY3QiLCAic2lnbmFsIiwgIk1vc2FpY0NsaWVudCIsICJjb3VudCIsICJRdWVyeSIsICJNb3NhaWNDbGllbnQiLCAic2lnbmFsIiwgIlNlbGVjdGlvbiIsICJjb2x1bW4iLCAiUXVlcnkiLCAiZXZlbnQiLCAiZm9ybWF0IiwgIlF1ZXJ5IiwgImVmZmVjdCJdCn0K
