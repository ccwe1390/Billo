"use strict";
// Billow demo dashboard: renders GET /stats with textContent only (no HTML injection path).

var COUNT_ROWS = [
  ["photos_read", "Photos read"],
  ["results_free_care", "Results: free care"],
  ["results_discount", "Results: discount"],
  ["results_not_eligible", "Results: not eligible"],
  ["packets", "Packets made"],
  ["fallbacks", "English fallbacks"],
  ["household_views", "Home views"],
  ["checks_run", "Bill checks run"],
  ["disputes", "Letters to the hospital"],
  ["eobs_read", "Insurance summaries read"]
];

function el(tag, text, cls) {
  var e = document.createElement(tag);
  if (text !== undefined && text !== null) { e.textContent = String(text); }
  if (cls) { e.className = cls; }
  return e;
}

function clear(node) {
  while (node.firstChild) { node.removeChild(node.firstChild); }
}

function table(headA, headB, rows) {
  var t = el("table");
  var hr = el("tr");
  hr.appendChild(el("th", headA));
  hr.appendChild(el("th", headB));
  t.appendChild(hr);
  rows.forEach(function (r) {
    var tr = el("tr");
    tr.appendChild(el("td", r[0]));
    tr.appendChild(el("td", r[1]));
    t.appendChild(tr);
  });
  return t;
}

function localToday() {
  var d = new Date();
  var m = String(d.getMonth() + 1);
  var day = String(d.getDate());
  return d.getFullYear() + "-" + (m.length < 2 ? "0" + m : m) + "-" + (day.length < 2 ? "0" + day : day);
}

function render(s) {
  var counts = document.getElementById("counts");
  var langs = document.getElementById("languages");
  var rules = document.getElementById("rules");
  var since = document.getElementById("since");
  clear(counts); clear(langs); clear(rules); clear(since);

  since.textContent = "Since " + s.since;

  counts.appendChild(el("h2", "Counts"));
  counts.appendChild(table("Measure", "Count", COUNT_ROWS.map(function (r) {
    return [r[1], (s.counts || {})[r[0]]];
  })));

  langs.appendChild(el("h2", "Languages"));
  var codes = Object.keys(s.languages || {}).sort();
  if (codes.length === 0) {
    langs.appendChild(el("p", "None yet"));
  } else {
    langs.appendChild(table("Language", "Count", codes.map(function (c) { return [c, s.languages[c]]; })));
  }

  rules.appendChild(el("h2", "Rules in use"));
  var ul = el("ul");
  (s.rules || []).forEach(function (r) {
    ul.appendChild(el("li", r.rule_en + " - " + r.source + ", page " + r.page + ", effective " + r.effective_date));
  });
  rules.appendChild(ul);
  var overdue = s.rules_review_by < localToday();
  rules.appendChild(el("p", "Review by " + s.rules_review_by, overdue ? "overdue" : ""));
}

function load() {
  fetch("/stats").then(function (resp) {
    if (!resp.ok) { throw new Error("HTTP " + resp.status); }
    return resp.json();
  }).then(render).catch(function () {
    var counts = document.getElementById("counts");
    clear(counts);
    counts.appendChild(el("p", "Could not load the dashboard."));
  });
}

document.getElementById("refresh").addEventListener("click", load);
load();
