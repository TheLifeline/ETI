module.exports = {
  root: true,

  env: {
    node: true
  },

  extends: [
    'plugin:vue/essential',
    '@vue/standard'
  ],

  parserOptions: {
    parser: 'babel-eslint'
  },

  rules: {
    'no-console': 'off',
    'no-debugger': 'off',
    'space-before-function-paren': 0,
    "comma-dangle": ["error", {
      "arrays": "ignore",
      "objects": "ignore",
      "imports": "never",
      "exports": "never",
      "functions": "ignore"
  }],
    'eol-last': "off"
  },

  'extends': [
    'plugin:vue/recommended',
    '@vue/standard'
  ]
}
