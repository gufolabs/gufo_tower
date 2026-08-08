// ----------------------------------------------------------------------
// ESLint configuration
// ----------------------------------------------------------------------
import eslint from "@eslint/js";

export default [
    {
        ignores: [
            "src/ui/pkg/**",
            "src/ui/pkg/**/*.js",
        ],
    },
    eslint.configs.recommended,
    {
        files: ["src/ui/**/*.js"],
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
            globals: {
                window: "readonly",
                navigator: "readonly",
                document: "readonly",
                console: "readonly",
                Notification: "readonly",
                XMLHttpRequest: "readonly",
                webix: "readonly",
                "$$": "readonly",
            },
        },
        rules: {
            "no-undef": "error",
            "no-unused-vars": [
                "warn",
                {
                    args: "none",
                    ignoreRestSiblings: true,
                },
            ],
            "eqeqeq": ["error", "always"],
            "curly": ["error", "all"],
            "no-var": "error",
            "prefer-const": "error",
        },
    },
];