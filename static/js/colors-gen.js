var Colors = function (hslLength) {
    this.hslLength = hslLength ? hslLength : 1;
    this.cArray = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
    this.hslArray = [];
};
//返回颜色数组
Colors.prototype.rgbArray = function () {
    var self = this;
    this.hslArray = this.getHslArray();
    if (!self.hslArray.length) return [];

    var rgbArray = self.hslArray.map(function (item) {
        return self.hslToRgb.apply(this, item);
    });

    return rgbArray.map(function (item) {
        return {
            //三原色值
            value: item,
            //16进制的颜色
            hex: self.rgbToHexadecimal(item),
            //rgb颜色
            rgb: 'rgb(' + item.toString() + ')',
            style: {
                background: 'rgb(' + item.toString() + ')'
            }
        }
    });
};
Colors.prototype.hexArray = function () {
    var self = this;
    this.hslArray = this.getHslArray();
    if (!self.hslArray.length) return [];

    var rgbArray = self.hslArray.map(function (item) {
        return self.hslToRgb.apply(this, item);
    });

    return rgbArray.map(function (item) {
        return self.rgbToHexadecimal(item)
    });
};
/**
 * RGB颜色转为16进制
 * @param {Object} item rgb颜色数组
 */
Colors.prototype.rgbToHexadecimal = function (item) {
    if (item && item.length == 3) {
        var a = item[0],
            b = item[1],
            c = item[2],
            d = "#",
            cArray = this.cArray;
        d += cArray[Math.floor(a / 16)] + "" + cArray[a % 16] + "";
        d += cArray[Math.floor(b / 16)] + "" + cArray[b % 16] + "";
        d += cArray[Math.floor(c / 16)] + "" + cArray[c % 16] + "";
        return d;
    }
};

/**
 * HSL颜色值转换为RGB
 * H，S，L 设定在 [0, 1] 之间
 * R，G，B 返回在 [0, 255] 之间
 *
 * @param H 色相
 * @param S 饱和度
 * @param L 亮度
 * @returns Array RGB色值
 */
Colors.prototype.hslToRgb = function (H, S, L) {
    var R, G, B;
    if (+S === 0) {
        R = G = B = L; // 饱和度为0 为灰色
    } else {
        var hue2Rgb = function (p, q, t) {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };
        var Q = L < 0.5 ? L * (1 + S) : L + S - L * S;
        var P = 2 * L - Q;
        R = hue2Rgb(P, Q, H + 1 / 3);
        G = hue2Rgb(P, Q, H);
        B = hue2Rgb(P, Q, H - 1 / 3);
    }
    return [Math.round(R * 255), Math.round(G * 255), Math.round(B * 255)];
};

// 获取随机HSL
Colors.prototype.randomHsl = function () {
    var H = Math.random();
    var S = Math.random();
    var L = Math.random();
    return [H, S, L];
}

// 获取HSL数组
Colors.prototype.getHslArray = function () {
    var HSL = [];
    var hslLength = this.hslLength ? this.hslLength : 1;
    for (var i = 0; i < hslLength; i++) {
        var ret = this.randomHsl();

        // 颜色相邻颜色差异须大于 0.25
        if (i > 0 && Math.abs(ret[0] - HSL[i - 1][0]) < 0.25) {
            i--;
            continue; // 重新获取随机色
        }
        ret[1] = 0.7 + (ret[1] * 0.2); // [0.7 - 0.9] 排除过灰颜色
        ret[2] = 0.4 + (ret[2] * 0.4); // [0.4 - 0.8] 排除过亮过暗色

        // 数据转化到小数点后两位
        ret = ret.map(function (item) {
            return parseFloat(item.toFixed(2));
        });

        HSL.push(ret);
    }
    return HSL;
};
var colorHash = new ColorHash();
 