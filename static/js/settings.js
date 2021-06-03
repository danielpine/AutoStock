var base_o_x = 370;
var base_o_y = 370;
var step = 110.5;
var STATUS = {
    NotConn: 0,
    AlreadyConn: 1
};
//随机生成name
//用于生成uuid
function guid() {
    return parseInt(Math.random() * 1000) + '';
}

function randomName() {
    return 'Nineuser-' + guid();
}

var rules =
    '<div class="layer_open"><p>双方各有九个棋子，轮流下到棋盘的空位上。<p>如果一方有三个棋子连成一线' +
    '，也就是形成一个工厂，就可以选择吃掉对方的一个棋子。<p>被吃的棋子不可以是位于' +
    '对方所形成的工厂之内，除非对方所有棋子都形成了工厂。<p>在九个棋子都布放到棋盘' +
    '上以后，可以沿棋盘上的线条移动到相邻的位置来形成厂以吃掉对方的棋子。<p>一个工' +
    '厂可以开开合合重复使用。<p>如果一方所剩下的棋子只有三个时，棋子可以“飞”到任' +
    '何位置而不受只能移动到相邻位置的限制。<p>当一方只剩下两个棋子或者他的所有棋子' +
    '都不能移动时就算输</div>';
var initmap = {
    11: {
        x: 1,
        y: 1,
        piece: 0
    },
    12: {
        x: 1,
        y: 2,
        piece: 0
    },
    13: {
        x: 1,
        y: 3,
        piece: 0
    },
    14: {
        x: 1,
        y: 4,
        piece: 0
    },
    15: {
        x: 1,
        y: 5,
        piece: 0
    },
    16: {
        x: 1,
        y: 6,
        piece: 0
    },
    17: {
        x: 1,
        y: 7,
        piece: 0
    },
    18: {
        x: 1,
        y: 8,
        piece: 0
    },
    21: {
        x: 2,
        y: 1,
        piece: 0
    },
    22: {
        x: 2,
        y: 2,
        piece: 0
    },
    23: {
        x: 2,
        y: 3,
        piece: 0
    },
    24: {
        x: 2,
        y: 4,
        piece: 0
    },
    25: {
        x: 2,
        y: 5,
        piece: 0
    },
    26: {
        x: 2,
        y: 6,
        piece: 0
    },
    27: {
        x: 2,
        y: 7,
        piece: 0
    },
    28: {
        x: 2,
        y: 8,
        piece: 0
    },
    31: {
        x: 3,
        y: 1,
        piece: 0
    },
    32: {
        x: 3,
        y: 2,
        piece: 0
    },
    33: {
        x: 3,
        y: 3,
        piece: 0
    },
    34: {
        x: 3,
        y: 4,
        piece: 0
    },
    35: {
        x: 3,
        y: 5,
        piece: 0
    },
    36: {
        x: 3,
        y: 6,
        piece: 0
    },
    37: {
        x: 3,
        y: 7,
        piece: 0
    },
    38: {
        x: 3,
        y: 8,
        piece: 0
    }
};

var position = {
    11: {
        top: base_o_x - 1 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    12: {
        top: base_o_x - 1 * step + 'px',
        left: base_o_y + 1 * step + 'px'
    },
    13: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y + 1 * step + 'px'
    },
    14: {
        top: base_o_x + 1 * step + 'px',
        left: base_o_y + 1 * step + 'px'
    },
    15: {
        top: base_o_x + 1 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    16: {
        top: base_o_x + 1 * step + 'px',
        left: base_o_y - 1 * step + 'px'
    },
    17: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y - 1 * step + 'px'
    },
    18: {
        top: base_o_x - 1 * step + 'px',
        left: base_o_y - 1 * step + 'px'
    },
    21: {
        top: base_o_x - 2 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    22: {
        top: base_o_x - 2 * step + 'px',
        left: base_o_y + 2 * step + 'px'
    },
    23: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y + 2 * step + 'px'
    },
    24: {
        top: base_o_x + 2 * step + 'px',
        left: base_o_y + 2 * step + 'px'
    },
    25: {
        top: base_o_x + 2 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    26: {
        top: base_o_x + 2 * step + 'px',
        left: base_o_y - 2 * step + 'px'
    },
    27: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y - 2 * step + 'px'
    },
    28: {
        top: base_o_x - 2 * step + 'px',
        left: base_o_y - 2 * step + 'px'
    },
    31: {
        top: base_o_x - 3 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    32: {
        top: base_o_x - 3 * step + 'px',
        left: base_o_y + 3 * step + 'px'
    },
    33: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y + 3 * step + 'px'
    },
    34: {
        top: base_o_x + 3 * step + 'px',
        left: base_o_y + 3 * step + 'px'
    },
    35: {
        top: base_o_x + 3 * step + 'px',
        left: base_o_y + 0 * step + 'px'
    },
    36: {
        top: base_o_x + 3 * step + 'px',
        left: base_o_y - 3 * step + 'px'
    },
    37: {
        top: base_o_x + 0 * step + 'px',
        left: base_o_y - 3 * step + 'px'
    },
    38: {
        top: base_o_x - 3 * step + 'px',
        left: base_o_y - 3 * step + 'px'
    }
};