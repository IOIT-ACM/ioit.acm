document.addEventListener("DOMContentLoaded", () => {
  const elements = {
    inputForm: document.getElementById("input-form"),
    generateBtn: document.getElementById("generate-btn"),
    generateBtnText: document.getElementById("generate-btn-text"),
    generateBtnLoadingText: document.getElementById(
      "generate-btn-loading-text",
    ),
    loadingSpinner: document.getElementById("loading-spinner"),
    outputContainer: document.getElementById("output-container"),
    linkedinOutput: document.getElementById("linkedin-output"),
    instagramOutput: document.getElementById("instagram-output"),
    whatsappOutput: document.getElementById("whatsapp-output"),
    settingsBtn: document.getElementById("settings-btn"),
    settingsModal: document.getElementById("settings-modal"),
    closeSettingsModalBtn: document.getElementById("close-settings-modal-btn"),
    saveSettingsBtn: document.getElementById("save-settings-btn"),
    clearApiKeyBtn: document.getElementById("clear-api-key-btn"),
    apiKeyInput: document.getElementById("api-key"),
    modelSelect: document.getElementById("model-select"),
    dynamicFieldsContainer: document.getElementById("dynamic-fields-container"),
    contextToolbar: document.getElementById("context-toolbar"),
    showPromptBtn: document.getElementById("show-prompt-btn"),
    promptContainer: document.getElementById("prompt-container"),
    promptDrawer: document.getElementById("prompt-drawer"),
    promptOverlay: document.getElementById("prompt-overlay"),
    promptContent: document.getElementById("prompt-content"),
    closePromptDrawerBtn: document.getElementById("close-prompt-drawer-btn"),
    copyPromptBtn: document.getElementById("copy-prompt-btn"),
    postContext: document.getElementById("post-context"),
    apiKeyPrompt: document.getElementById("api-key-prompt"),
  };

  let contactCount = 0;
  const MAX_CONTACTS = 2;
  let lastGeneratedPrompt = "";

  const checkApiKeyPresence = () => {
    const apiKey = localStorage.getItem("geminiApiKey");
    if (elements.apiKeyPrompt) {
      elements.apiKeyPrompt.classList.toggle("hidden", !!apiKey);
    }
  };

  const validateInputs = () => {
    if (!elements.generateBtn || !elements.postContext) return;
    let isFormValid = true;
    if (elements.postContext.value.trim() === "") isFormValid = false;
    const dynamicFields = document.querySelectorAll(".dynamic-field-wrapper");
    dynamicFields.forEach((field) => {
      if (!isFormValid) return;
      const fieldType = field.dataset.fieldType;
      switch (fieldType) {
        case "instructions":
          const instructions = field.querySelector("#special-instructions");
          if (!instructions || instructions.value.trim() === "")
            isFormValid = false;
          break;
        case "datetime":
          const date = field.querySelector("#event-date");
          const time = field.querySelector("#event-time");
          if (
            (!date || date.value.trim() === "") &&
            (!time || time.value.trim() === "")
          )
            isFormValid = false;
          break;
        case "venue":
          const venue = field.querySelector("#event-venue");
          if (!venue || venue.value.trim() === "") isFormValid = false;
          break;
        case "registration":
          const regLink = field.querySelector("#reg-link");
          if (!regLink || regLink.value.trim() === "") isFormValid = false;
          break;
        case "prizes":
          const prizes = field.querySelector("#prizes");
          if (!prizes || prizes.value.trim() === "") isFormValid = false;
          break;
        case "contact":
          const name = field.querySelector(".contact-name");
          const mobile = field.querySelector(".contact-mobile");
          if (
            (!name || name.value.trim() === "") &&
            (!mobile || mobile.value.trim() === "")
          )
            isFormValid = false;
          break;
      }
    });
    elements.generateBtn.disabled = !isFormValid;
  };

  const loadSettings = () => {
    if (elements.apiKeyInput)
      elements.apiKeyInput.value = localStorage.getItem("geminiApiKey") || "";
    if (elements.modelSelect)
      elements.modelSelect.value =
        localStorage.getItem("geminiModel") || "gemini-2.5-flash";
  };

  const saveSettings = () => {
    if (!elements.apiKeyInput || !elements.modelSelect) return;
    const apiKey = elements.apiKeyInput.value.trim();
    if (apiKey) {
      localStorage.setItem("geminiApiKey", apiKey);
      localStorage.setItem("geminiModel", elements.modelSelect.value);
      alert("Settings saved successfully.");
      toggleModal(elements.settingsModal, false);
      checkApiKeyPresence();
    } else alert("Please enter a valid API Key.");
  };

  const clearApiKey = () => {
    localStorage.removeItem("geminiApiKey");
    if (elements.apiKeyInput) elements.apiKeyInput.value = "";
    alert("API Key cleared.");
    checkApiKeyPresence();
  };

  const toggleModal = (modal, show) => {
    if (!modal) return;
    modal.classList.toggle("hidden", !show);
  };

  const togglePromptDrawer = (show) => {
    if (show) {
      elements.promptContainer.classList.remove("hidden");
      requestAnimationFrame(() =>
        elements.promptContainer.classList.add("is-open"),
      );
    } else {
      elements.promptContainer.classList.remove("is-open");
      setTimeout(() => elements.promptContainer.classList.add("hidden"), 300);
    }
  };

  const getFieldHTML = (fieldType) => {
    switch (fieldType) {
      case "instructions":
        return `
          <label for="special-instructions" class="form-label block mb-2">Special Instructions</label>
          <textarea id="special-instructions" rows="3" class="form-textarea w-full"></textarea>`;
      case "datetime":
        return `
          <label class="form-label block mb-2">Date & Time</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input type="date" id="event-date" class="form-input w-full">
            <input type="time" id="event-time" class="form-input w-full">
          </div>`;
      case "venue":
        return `
          <label for="event-venue" class="form-label block mb-2">Venue / Platform</label>
          <input type="text" id="event-venue" class="form-input w-full">`;
      case "registration":
        return `
          <label for="reg-link" class="form-label block mb-2">Registration Link</label>
          <input type="url" id="reg-link" class="form-input w-full">`;
      case "prizes":
        return `
          <label for="prizes" class="form-label block mb-2">Prizes</label>
          <input type="text" id="prizes" class="form-input w-full">`;
      case "contact":
        contactCount++;
        return `
          <label class="form-label block mb-2">Contact Person ${contactCount}</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input type="text" class="form-input contact-name" placeholder="Name">
            <input type="tel" class="form-input contact-mobile" placeholder="Mobile">
          </div>`;
      default:
        return "";
    }
  };

  const addField = (fieldType) => {
    if (fieldType === "contact" && contactCount >= MAX_CONTACTS) {
      alert(`You can add a maximum of ${MAX_CONTACTS} contacts.`);
      return;
    }
    const wrapper = document.createElement("div");
    wrapper.className = "relative pt-2 dynamic-field-wrapper";
    wrapper.dataset.fieldType = fieldType;
    wrapper.innerHTML = `
      <button class="remove-field-btn absolute top-0 right-0 text-gray-500 hover:text-white">
        <i data-lucide="x-circle" class="w-5 h-5"></i>
      </button>
      ${getFieldHTML(fieldType)}
    `;
    elements.dynamicFieldsContainer.appendChild(wrapper);
    if (typeof lucide !== "undefined") lucide.createIcons();
    const button = elements.contextToolbar.querySelector(
      `[data-field-type="${fieldType}"]`,
    );
    if (button) {
      if (fieldType !== "contact" || contactCount >= MAX_CONTACTS)
        button.disabled = true;
    }
    validateInputs();
  };

  const removeField = (fieldWrapper) => {
    const fieldType = fieldWrapper.dataset.fieldType;
    if (fieldType === "contact") contactCount--;
    fieldWrapper.remove();
    const button = elements.contextToolbar.querySelector(
      `[data-field-type="${fieldType}"]`,
    );
    if (button) button.disabled = false;
    validateInputs();
  };

  const constructPrompt = () => {
    const getVal = (selector) => {
      const el = document.querySelector(selector);
      return el ? el.value.trim() : "";
    };
    const categoryEl = document.querySelector(
      'input[name="post-category"]:checked',
    );
    const category = categoryEl ? categoryEl.value : "General Post";

    let variableSection = `// VARIABLE\n`;
    variableSection += `[Post Context]: Category: ${category}. Details: ${getVal("#post-context")}\n`;
    let keyInfoParts = [];
    if (getVal("#event-date"))
      keyInfoParts.push(`Date: ${getVal("#event-date")}`);
    if (getVal("#event-time"))
      keyInfoParts.push(`Time: ${getVal("#event-time")}`);
    if (getVal("#event-venue"))
      keyInfoParts.push(`Venue/Platform: ${getVal("#event-venue")}`);
    if (getVal("#reg-link"))
      keyInfoParts.push(`Registration Link: ${getVal("#reg-link")}`);
    if (getVal("#prizes")) keyInfoParts.push(`Prizes: ${getVal("#prizes")}`);
    const contacts = Array.from(document.querySelectorAll(".contact-name"))
      .map((el, i) => {
        const mobileEl = document.querySelectorAll(".contact-mobile")[i];
        const name = el.value.trim();
        const mobile = mobileEl ? mobileEl.value.trim() : "";
        return name && mobile ? `${name} (${mobile})` : null;
      })
      .filter(Boolean);
    if (contacts.length > 0)
      keyInfoParts.push(`Contact: ${contacts.join(", ")}`);
    if (keyInfoParts.length > 0)
      variableSection += `[Key Information]: ${keyInfoParts.join(". ")}\n`;
    const specialInstructions = getVal("#special-instructions");
    if (specialInstructions)
      variableSection += `[Special Instructions]: ${specialInstructions}\n`;

    const basePrompt = `
// ROLE
You are an expert social media content creator and marketing strategist, specializing in crafting engaging and platform-specific content for technology-focused student organization AISSMS IOIT ACM Student Chapter.

// INSTRUCTION
Based on the provided context, and special instructions, generate three distinct and tailored captions for a social media post. The captions should be for LinkedIn, Instagram, and a WhatsApp message, respectively. Your primary goal is to promote the AISSMS IOIT ACM Student Chapter and its activities, driving engagement and participation. Generate the LinkedIn caption first, then Instagram, then WhatsApp.

// CONTEXT
The AISSMS IOIT ACM Student Chapter is a student-run organization at the AISSMS Institute of Information Technology. It focuses on advancing computing as a science and profession. The target audience includes students, faculty, and tech enthusiasts. The tone should be professional yet approachable, informative, and inspiring.

// CONSTRAINT
You must adhere to the following platform-specific formatting and style guidelines:
- **LinkedIn:** Maintain a professional and informative tone. Use relevant professional hashtags (e.g., #ACM, #ComputerScience, #TechStudents). For bullet points, you MUST use the '•' (U+2022) character, not hyphens or asterisks.
- **Instagram:** Use a more conversational, energetic, and visually-driven tone. Include engaging questions to encourage comments. Use a mix of relevant, popular, and niche hashtags. Incorporate emojis where appropriate to increase visual appeal.
- **WhatsApp:** Craft a concise, clear, and direct message suitable for broadcast lists or status updates. Use emojis to add a friendly touch and ensure key information is easy to scan. Always include a clear call-to-action. For emphasis, you MUST use single asterisks for bold (e.g., *important*) and single underscores for italics (e.g., _note_). For lists, you MUST use hyphens (e.g., - Point 1). The whatsapp messages shal end with Best Regards, AISSMS IOIT ACM Student Chapter.
Do not include any other text, preamble, or explanation in your response. Only output the three captions, each starting with "**LinkedIn Caption:**", "**Instagram Caption:**", and "**WhatsApp Caption:**" respectively.
`;

    lastGeneratedPrompt = `${basePrompt}\n${variableSection}`;
    return lastGeneratedPrompt;
  };

  const displayStreamedResults = (text) => {
    const captions = { linkedin: "", instagram: "", whatsapp: "" };

    const instaHeader = "**Instagram Caption:**";
    const whatsappHeader = "**WhatsApp Caption:**";
    const linkedinHeader = "**LinkedIn Caption:**";
    const whatsappHeaderAlt = "**WhatsApp Message:**";

    let remainingText = text;

    const instaIndex = remainingText.indexOf(instaHeader);
    const whatsappIndex =
      remainingText.indexOf(whatsappHeader) > -1
        ? remainingText.indexOf(whatsappHeader)
        : remainingText.indexOf(whatsappHeaderAlt);

    let linkedinText = remainingText;
    if (instaIndex !== -1) {
      linkedinText = remainingText.substring(0, instaIndex);
    } else if (whatsappIndex !== -1) {
      linkedinText = remainingText.substring(0, whatsappIndex);
    }
    captions.linkedin = linkedinText.replace(linkedinHeader, "").trim();
    elements.linkedinOutput.innerHTML = captions.linkedin.replace(
      /\n/g,
      "<br>",
    );

    if (instaIndex !== -1) {
      let instagramText = remainingText.substring(instaIndex);
      if (whatsappIndex !== -1 && whatsappIndex > instaIndex) {
        instagramText = remainingText.substring(instaIndex, whatsappIndex);
      }
      captions.instagram = instagramText.replace(instaHeader, "").trim();
      elements.instagramOutput.innerHTML = captions.instagram.replace(
        /\n/g,
        "<br>",
      );
    }

    if (whatsappIndex !== -1) {
      let whatsappText = remainingText.substring(whatsappIndex);
      captions.whatsapp = whatsappText
        .replace(whatsappHeader, "")
        .replace(whatsappHeaderAlt, "")
        .trim();
      const formattedWhatsapp = captions.whatsapp
        .replace(/\*(.*?)\*/g, "<b>$1</b>")
        .replace(/_(.*?)_/g, "<i>$1</i>")
        .replace(/\n/g, "<br>");
      elements.whatsappOutput.innerHTML = formattedWhatsapp;
    }

    return captions;
  };

  const generateCaptions = async () => {
    const apiKey = localStorage.getItem("geminiApiKey");
    if (!apiKey) {
      alert("Please set your Gemini API Key in the settings.");
      toggleModal(elements.settingsModal, true);
      return;
    }
    const model = localStorage.getItem("geminiModel");
    const promptText = constructPrompt();
    const requestBody = { contents: [{ parts: [{ text: promptText }] }] };

    elements.generateBtn.disabled = true;
    elements.generateBtnText.classList.add("hidden");
    elements.generateBtnLoadingText.classList.remove("hidden");
    elements.loadingSpinner.classList.remove("hidden");

    elements.outputContainer.classList.remove("hidden");
    elements.linkedinOutput.innerHTML = "";
    elements.instagramOutput.innerHTML = "";
    elements.whatsappOutput.innerHTML = "";

    let fullGeneratedText = "";
    let finalCaptions = {};

    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestBody),
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message || "API request failed");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const regex = /"text"\s*:\s*"((?:\\.|[^"\\])*)"/g;
        let match;
        while ((match = regex.exec(chunk)) !== null) {
          const text = match[1]
            .replace(/\\"/g, '"')
            .replace(/\\n/g, "\n")
            .replace(/\\\\/g, "\\");
          fullGeneratedText += text;
          finalCaptions = displayStreamedResults(fullGeneratedText);
        }
      }

      elements.linkedinOutput.dataset.copyText = finalCaptions.linkedin || "";
      elements.instagramOutput.dataset.copyText = finalCaptions.instagram || "";
      elements.whatsappOutput.dataset.copyText = finalCaptions.whatsapp || "";
    } catch (error) {
      alert(`An error occurred: ${error.message}`);
      elements.outputContainer.classList.add("hidden");
    } finally {
      elements.generateBtnText.classList.remove("hidden");
      elements.generateBtnLoadingText.classList.add("hidden");
      elements.loadingSpinner.classList.add("hidden");
      validateInputs();
    }
  };

  const copyToClipboard = (event) => {
    const button = event.currentTarget;
    const targetId = button.dataset.target;
    const targetElement = document.getElementById(targetId);
    const textToCopy =
      targetElement.dataset.copyText || targetElement.textContent;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const span = button.querySelector("span");
      const originalText = span.textContent;
      span.textContent = "Copied!";
      setTimeout(() => (span.textContent = originalText), 2000);
    });
  };

  elements.generateBtn.addEventListener("click", generateCaptions);
  elements.settingsBtn.addEventListener("click", () =>
    toggleModal(elements.settingsModal, true),
  );
  elements.closeSettingsModalBtn.addEventListener("click", () =>
    toggleModal(elements.settingsModal, false),
  );
  elements.saveSettingsBtn.addEventListener("click", saveSettings);
  elements.clearApiKeyBtn.addEventListener("click", clearApiKey);

  elements.contextToolbar.addEventListener("click", (e) => {
    const button = e.target.closest(".context-btn");
    if (button && !button.disabled) addField(button.dataset.fieldType);
  });

  elements.dynamicFieldsContainer.addEventListener("click", (e) => {
    const button = e.target.closest(".remove-field-btn");
    if (button) removeField(button.parentElement);
  });

  elements.showPromptBtn.addEventListener("click", () => {
    const prompt = constructPrompt();
    elements.promptContent.textContent = prompt;
    togglePromptDrawer(true);
  });

  elements.closePromptDrawerBtn.addEventListener("click", () =>
    togglePromptDrawer(false),
  );
  elements.promptOverlay.addEventListener("click", () =>
    togglePromptDrawer(false),
  );

  elements.copyPromptBtn.addEventListener("click", () => {
    const prompt = lastGeneratedPrompt || constructPrompt();
    navigator.clipboard.writeText(prompt).then(() => {
      const span = elements.copyPromptBtn.querySelector("span");
      const originalText = span.textContent;
      span.textContent = "Copied!";
      setTimeout(() => (span.textContent = originalText), 2000);
    });
  });

  if (elements.inputForm)
    elements.inputForm.addEventListener("input", validateInputs);

  document
    .querySelectorAll(".copy-btn")
    .forEach((btn) => btn.addEventListener("click", copyToClipboard));

  loadSettings();
  validateInputs();
  checkApiKeyPresence();
  if (typeof lucide !== "undefined") lucide.createIcons();
});
