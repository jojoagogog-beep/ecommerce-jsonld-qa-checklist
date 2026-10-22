/* Practical AI Lab: dependency-free, local-only IMG alt attribute inspector.
 * Does not execute scripts, create live IMG elements, or request src URLs.
 */
(function (root) {
  "use strict";
  function parseAttributes(tag) {
    const attributes = Object.create(null);
    let i = 4;
    while (i < tag.length) {
      while (i < tag.length && /[\s/>]/.test(tag[i])) i++;
      if (i >= tag.length) break;
      let name = "";
      while (i < tag.length && /[^\s=/>]/.test(tag[i])) name += tag[i++];
      if (!name) { i++; continue; }
      while (i < tag.length && /\s/.test(tag[i])) i++;
      let value = "";
      if (tag[i] === "=") {
        i++;
        while (i < tag.length && /\s/.test(tag[i])) i++;
        if (tag[i] === "'" || tag[i] === '"') {
          const quote = tag[i++];
          while (i < tag.length && tag[i] !== quote) value += tag[i++];
          if (tag[i] === quote) i++;
        } else {
          while (i < tag.length && /[^\s>]/.test(tag[i])) value += tag[i++];
        }
      }
      if (!(name.toLowerCase() in attributes)) attributes[name.toLowerCase()] = value;
    }
    return attributes;
  }
  function findImgTags(source) {
    const found = [];
    const input = String(source || "");
    let i = 0, suppressed = "";
    while (i < input.length) {
      const begin = input.indexOf("<", i);
      if (begin < 0) break;
      if (input.startsWith("<!--", begin)) {
        const end = input.indexOf("-->", begin + 4);
        i = end < 0 ? input.length : end + 3;
        continue;
      }
      if (suppressed) {
        const closing = new RegExp("^<\\s*\\/\\s*" + suppressed + "\\b", "i");
        if (!closing.test(input.slice(begin, begin + 35))) {
          i = begin + 1;
          continue;
        }
        suppressed = "";
      }
      const name = /^<\s*(\/?)([a-z][\w:-]*)\b/i.exec(input.slice(begin, begin + 55));
      if (!name) { i = begin + 1; continue; }
      let pos = begin + name[0].length, quote = "";
      while (pos < input.length) {
        const ch = input[pos++];
        if (quote) {
          if (ch === quote) quote = "";
        } else if (ch === "'" || ch === '"') {
          quote = ch;
        } else if (ch === ">") break;
      }
      if (input[pos - 1] !== ">") break;
      const tag = input.slice(begin, pos);
      i = pos;
      if (!name[1] && ["script", "style", "textarea", "title"].includes(name[2].toLowerCase())) suppressed = name[2].toLowerCase();
      if (!name[1] && name[2].toLowerCase() === "img") found.push(tag);
    }
    return found;
  }
  const weakLabels = /^(?:img|image|photo|picture|graphic|icon|thumbnail|untitled|product image|product photo|image of)$/i;
  const filenameLike = /(?:^|[/\\])[^\s]+\.(?:png|jpe?g|webp|gif|svg|avif)(?:\?.*)?$/i;
  function check(source) {
    const tags = findImgTags(source);
    const rows = tags.map((tag, idx) => {
      const attrs = parseAttributes(tag);
      const hasAlt = Object.hasOwn(attrs, "alt");
      const alt = (attrs.alt || "").trim();
      let status, note, severity;
      if (!hasAlt) {
        status = "Missing alt"; severity = "review";
        note = 'Add descriptive alt text for informative images, or alt="" for decorative images.';
      } else if (!alt) {
        status = "Empty alt"; severity = "informational";
        note = "May be appropriate if the image is purely decorative; review its context.";
      } else if (weakLabels.test(alt) || filenameLike.test(alt) || /^image\s*\d+$/i.test(alt)) {
        status = "Weak alt candidate"; severity = "review";
        note = "Replace vague labels or filenames with a concise description of the image's purpose.";
      } else {
        status = "Alt present"; severity = "informational";
        note = "Text exists; semantic quality and surrounding content still require human review.";
      }
      if (!Object.hasOwn(attrs, "src") && !Object.hasOwn(attrs, "srcset")) note += " No src/srcset was declared.";
      return { index: idx + 1, source: attrs.src || attrs.srcset || "(no src)", alt: hasAlt ? attrs.alt : null,
               status, severity, note };
    });
    return {
      total: rows.length,
      missing: rows.filter(r => r.status === "Missing alt").length,
      empty: rows.filter(r => r.status === "Empty alt").length,
      weak: rows.filter(r => r.status === "Weak alt candidate").length,
      present: rows.filter(r => r.status === "Alt present").length,
      rows
    };
  }
  const api = {check, parseAttributes, findImgTags};
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.PALImageAltAuditor = api;
})(typeof window !== "undefined" ? window : null);
