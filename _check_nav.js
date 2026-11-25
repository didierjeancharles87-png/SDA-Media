const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
// Find all nav links
let ni = 0;
while ((ni = c.indexOf('title="', ni)) !== -1) {
  let ti = ni + 7;
  let te = c.indexOf('"', ti);
  if (te > ti) {
    let title = c.substring(ti, te);
    let aEnd = c.indexOf('</a>', te);
    if (aEnd > te && aEnd - te < 100) {
      let content = c.substring(te + 1, aEnd).trim();
      console.log(title + ' -> ' + JSON.stringify(content) + ' (chars: ' + content.length + ')');
    }
  }
  ni = te + 1;
}
