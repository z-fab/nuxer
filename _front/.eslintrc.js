// .eslintrc.js
module.exports = {
    parser: "@typescript-eslint/parser",
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:react/recommended",
        "plugin:react-hooks/recommended",
        "plugin:jsx-a11y/recommended",
    ],
    plugins: ["@typescript-eslint", "react", "react-hooks", "jsx-a11y"],
    env: {
        browser: true,
        es6: true,
        node: true,
    },
    settings: {
        react: {
            version: "detect",
        },
    },

    // Configuração para usar 4 espaços para indentação
    indent: ["error", 4],
    "@typescript-eslint/indent": ["error", 4],

    // Outras regras comuns
    quotes: ["error", "single"],
    semi: ["error", "always"],
    "comma-dangle": ["error", "always-multiline"],
    "no-console": ["warn", { allow: ["warn", "error"] }],

    // Regras React
    "react/react-in-jsx-scope": "off", // Não é necessário em Next.js
    "react/prop-types": "off", // Não é necessário com TypeScript

    // Você pode adicionar mais regras conforme necessário

    ignorePatterns: ["node_modules/", ".next/", "out/"],
};
