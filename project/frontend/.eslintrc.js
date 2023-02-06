module.exports = {
    root: true,
    parserOptions: {
        parser: 'babel-eslint'
    },
    env: {
        browser: true,
        node: true,
    },
    extends: [
        'eslint:recommended',
        'plugin:vue/essential'
    ],
    rules: {
        'curly': ['error' ,'all'], //强制所有控制语句使用一致的括号风格
        'no-trailing-spaces': 'off', //禁用行尾空格
        'indent': ['error', 4], //强制使用一致的缩进
        'quotes': 'off', //强制使用一致的反勾号、双引号或单引号
        'spaced-comment': 'off', //强制在注释中 // 或 /* 使用一致的空格
        'eol-last': 'off', //要求或禁止文件末尾存在空行
        'padded-blocks': ['error', 'never'], //要求或禁止块内填充
        'camelcase': ['error', {"properties": "always"}] // 强制使用骆驼拼写法命名约定
    }
}