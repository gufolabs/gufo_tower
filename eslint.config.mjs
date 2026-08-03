// ----------------------------------------------------------------------
// ESLint configuration
// ----------------------------------------------------------------------

export default [
    {
        files: ["src/ui/**/*.js"],
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
            globals: {
                window: "readonly",
                document: "readonly",
                console: "readonly",
                webix: "readonly",
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