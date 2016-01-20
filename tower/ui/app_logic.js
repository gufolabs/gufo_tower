var app_logic = {
    current_env: null,

    init: function () {
        // Build UI objects
        webix.ui(app_ui);
        // Initialize appropriative controllers
        login_logic.init();
        change_password_logic.init();
        desktop_logic.init();
        // Process login sequence
        app_logic.process_login();
    },

    process_login: function () {
        // Check user is logged in
        API.login.is_logged().then(
            function (result) {
                if (result) {
                    desktop_logic.show();
                } else {
                    login_logic.show();
                }
            }, function (err) {
                Tower.msg.failed("Failed to connect to server");
                login_logic.show();
            }
        );
    },

    select_environment: function (env) {
        app_logic.current_env = env;
        desktop_logic.select_environment(env);
    },

    logout: function () {
        API.login.logout().then(
            function () {
                login_logic.show();
                Tower.msg.complete("Logged out");
            },
            function () {
                Tower.msg.failed("Failed to log out");
            }
        );
    }
};
