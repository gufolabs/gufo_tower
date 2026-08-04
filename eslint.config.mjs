// ----------------------------------------------------------------------
// ESLint configuration
// ----------------------------------------------------------------------

export default [
    {
        files: ["src/ui/**/*.js"],
        ignores: [
            "src/ui/pkg/**",
        ],
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
                Tower: "readonly",
                SDL: "readonly",
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
        },
    },
];