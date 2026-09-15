document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".subscribe-trigger").forEach(function (trigger) {
        const widget = trigger.closest(".subscribe-widget");
        const container = widget.querySelector(".subscribe-form-container");
        if (!container) return;

        trigger.addEventListener("click", function () {
            container.classList.toggle("hidden");
            if (!container.classList.contains("hidden")) {
                const emailInput = container.querySelector(".subscribe-email");
                if (emailInput) emailInput.focus();
            }
        });
    });

    document.querySelectorAll(".subscribe-form").forEach(function (subForm) {
        const widget = subForm.closest(".subscribe-widget") || subForm.parentElement;
        const emailInput = subForm.querySelector(".subscribe-email");
        const submitBtn = subForm.querySelector(".subscribe-btn");
        const msgBox = widget.querySelector(".subscribe-message");

        subForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = emailInput.value.trim();

            if (!email) return;

            submitBtn.disabled = true;
            submitBtn.classList.add("opacity-50", "cursor-not-allowed");

            fetch("/events/subscribe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ email: email })
            })
            .then(res => res.json())
            .then(data => {
                msgBox.classList.remove("hidden", "subscribe-msg-success", "subscribe-msg-warning", "subscribe-msg-error");
                msgBox.classList.add("font-bold", "shadow-lg");
                if (data.success) {
                    if (data.message.includes("already subscribed")) {
                        msgBox.classList.add("subscribe-msg-warning");
                        msgBox.innerHTML = `<i class="fas fa-info-circle mr-2"></i><span>${data.message}</span>`;
                    } else {
                        msgBox.classList.add("subscribe-msg-success");
                        msgBox.innerHTML = `<i class="fas fa-check-circle mr-2"></i><span>${data.message}</span>`;
                        emailInput.value = "";
                    }
                    subForm.classList.add("hidden");
                } else {
                    msgBox.classList.add("subscribe-msg-error");
                    msgBox.innerHTML = `<i class="fas fa-exclamation-circle mr-2"></i><span>${data.error || "Subscription failed. Please try again."}</span>`;
                }
            })
            .catch(() => {
                msgBox.classList.remove("hidden");
                msgBox.classList.add("subscribe-msg-error", "font-bold");
                msgBox.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i><span>An error occurred. Please try again.</span>`;
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.classList.remove("opacity-50", "cursor-not-allowed");
            });
        });
    });
});
