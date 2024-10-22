import os
import shutil

# Define the project directory
project_dir = "basecamp_bridge_extension"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# Copy the BCB.png file into the project directory
bcb_image_src = "BCB.png"
bcb_image_dst = os.path.join(project_dir, "BCB.png")
if os.path.exists(bcb_image_src):
    shutil.copy(bcb_image_src, bcb_image_dst)
else:
    print("Warning: 'BCB.png' file not found. Make sure it's in the same directory as this script.")

# manifest.json content with the icon included
manifest_content = '''{
  "manifest_version": 3,
  "name": "Basecamp Bridge Extension",
  "version": "2.1",
  "description": "Inserts predefined text, rewrites highlighted text using OpenAI API, simplifies English text, and allows quick access to project files.",
  "permissions": ["storage", "scripting", "clipboardWrite"],
  "host_permissions": ["https://api.openai.com/*", "https://*.basecamp.com/*"],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["https://*.basecamp.com/*"],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ],
  "web_accessible_resources": [
    {
      "resources": ["BCB.png"],
      "matches": ["<all_urls>"]
    }
  ],
  "icons": {
    "16": "BCB.png",
    "48": "BCB.png",
    "128": "BCB.png"
  }
}
'''

# content.js content with updated functionality and correct code
content_js_content = '''
let lastFocusedElement = null;

document.addEventListener('focus', function(e) {
    if (
        e.target.tagName === 'INPUT' ||
        e.target.tagName === 'TEXTAREA' ||
        e.target.isContentEditable
    ) {
        lastFocusedElement = e.target;
    }
}, true);

const guiContainer = document.createElement('div');
guiContainer.style.position = 'fixed';
guiContainer.style.bottom = '10px';
guiContainer.style.right = '10px';
guiContainer.style.backgroundColor = 'rgba(200, 200, 200, 0.9)';
guiContainer.style.color = 'black';
guiContainer.style.padding = '10px';
guiContainer.style.borderRadius = '5px';
guiContainer.style.fontSize = '16px';
guiContainer.style.zIndex = '10000';
guiContainer.style.display = 'flex';
guiContainer.style.flexDirection = 'column';
guiContainer.style.alignItems = 'center';
guiContainer.style.width = '200px';

// Add header image (BCB.png)
const logoImage = document.createElement('img');
logoImage.src = chrome.runtime.getURL('BCB.png');
logoImage.style.width = '100%';
logoImage.style.height = 'auto';
logoImage.style.marginBottom = '10px';
guiContainer.appendChild(logoImage);

const title = document.createElement('div');
title.textContent = 'BASECAMP BRIDGE';
title.style.marginBottom = '10px';
title.style.fontWeight = 'bold';
guiContainer.appendChild(title);

const jumpToFilesButton = document.createElement('button');
jumpToFilesButton.textContent = 'Jump To Files';
jumpToFilesButton.style.padding = '5px 10px';
jumpToFilesButton.style.fontSize = '14px';
jumpToFilesButton.style.cursor = 'pointer';
jumpToFilesButton.style.backgroundColor = '#007bff'; // Blue
jumpToFilesButton.style.color = 'white';
jumpToFilesButton.style.border = 'none';
jumpToFilesButton.style.borderRadius = '3px';
jumpToFilesButton.style.marginBottom = '5px';

jumpToFilesButton.addEventListener('click', function() {
    const currentUrl = window.location.href;
    const basecampRegex = /https:\\/\\/3\\.basecamp\\.com\\/(\\d+)\\/(?:projects|buckets)\\/(\\d+)/;
    const matches = currentUrl.match(basecampRegex);

    if (matches && matches.length === 3) {
        const baseId = matches[1];
        const projectId = matches[2];
        const newUrl = `https://3.basecamp.com/${baseId}/search?bucket_id=${projectId}&type=Attachment`;
        window.location.href = newUrl;
    } else {
        alert('This button works only on project-specific pages.');
    }
});

const insertTextButton = document.createElement('button');
insertTextButton.textContent = 'Insert KO Template';
insertTextButton.style.padding = '5px 10px';
insertTextButton.style.fontSize = '14px';
insertTextButton.style.cursor = 'pointer';
insertTextButton.style.backgroundColor = '#17a2b8'; // Turquoise
insertTextButton.style.color = 'white';
insertTextButton.style.border = 'none';
insertTextButton.style.borderRadius = '3px';
insertTextButton.style.marginBottom = '5px';

insertTextButton.addEventListener('click', function() {
    if (lastFocusedElement) {
        const textToInsert = `TITLE: XXX-XXX - PROJECT TITLE HERE KO

***Please DO NOT Reply or COMMENT against this MESSAGE***
Hi Team,
We have a fantastic opportunity to work on a line of new retail displays. They will be deployed to retail stores in the United States. The customer has requested that these displays be value engineered, and modular in-order to fit a wide variety of different products in the future. Looking forward to working with you all on this project!

(PLEASE ADD BRIEF PROJECT OVERVIEW HERE, RE-ORDER, NEW DEV, EMINENT ORDER P/O PENDING ETC)

-PM

[INSERT PPTX HERE]

CHERRY: Please assign the PM resource to the project and send your IPQL against the To-Do as soon as possible.
JACKIE, JAKE, PAIGE AND TONY: Please assign your department resource.

Thanks!`;

        if (lastFocusedElement.tagName === 'INPUT') {
            alert('Cannot insert multi-line text into an input field. Please use a textarea or contenteditable element.');
        } else if (lastFocusedElement.tagName === 'TEXTAREA' || lastFocusedElement.isContentEditable) {
            insertTextAtCursor(lastFocusedElement, textToInsert);
        } else {
            alert('The last focused element is not a text input.');
        }
    } else {
        alert('No text input has been focused yet.');
    }
});

function insertTextAtCursor(element, text) {
    if (element.tagName === 'TEXTAREA') {
        const startPos = element.selectionStart || 0;
        const endPos = element.selectionEnd || 0;
        const originalValue = element.value;
        element.value = originalValue.substring(0, startPos) + text + originalValue.substring(endPos);
        const newCursorPos = startPos + text.length;
        element.setSelectionRange(newCursorPos, newCursorPos);
        element.focus();
    } else if (element.isContentEditable) {
        const textWithLineBreaks = text.replace(/\\n/g, '<br>');
        const tempElement = document.createElement('div');
        tempElement.innerHTML = textWithLineBreaks;
        const frag = document.createDocumentFragment();
        let node;
        while ((node = tempElement.firstChild)) {
            frag.appendChild(node);
        }
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(frag);
        // Move cursor to the end of inserted content
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);
    }
}

const rewritePositiveButton = document.createElement('button');
rewritePositiveButton.textContent = 'Rewrite +';
rewritePositiveButton.style.padding = '5px 10px';
rewritePositiveButton.style.fontSize = '14px';
rewritePositiveButton.style.cursor = 'pointer';
rewritePositiveButton.style.backgroundColor = '#28a745'; // Green
rewritePositiveButton.style.color = 'white';
rewritePositiveButton.style.border = 'none';
rewritePositiveButton.style.borderRadius = '3px';
rewritePositiveButton.style.marginBottom = '5px';

rewritePositiveButton.addEventListener('click', function() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        chrome.runtime.sendMessage({ action: 'rewrite_positive', text: selectedText }, function(response) {
            if (response && response.rewrite) {
                const rewrittenText = response.rewrite;

                // Automatically copy the rewritten text to the clipboard
                navigator.clipboard.writeText(rewrittenText).then(function() {
                    alert('Rewritten Text (Positive):\\n\\n' + rewrittenText + '\\n\\n(Copied to clipboard)');
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                    alert('Rewritten Text (Positive):\\n\\n' + rewrittenText);
                });
            } else {
                alert('Failed to get rewrite: ' + (response.error || 'Unknown error.'));
            }
        });
    } else {
        alert('No text is highlighted.');
    }
});

const rewriteNeutralButton = document.createElement('button');
rewriteNeutralButton.textContent = 'Rewrite +/-';
rewriteNeutralButton.style.padding = '5px 10px';
rewriteNeutralButton.style.fontSize = '14px';
rewriteNeutralButton.style.cursor = 'pointer';
rewriteNeutralButton.style.backgroundColor = '#28a745'; // Green
rewriteNeutralButton.style.color = 'white';
rewriteNeutralButton.style.border = 'none';
rewriteNeutralButton.style.borderRadius = '3px';
rewriteNeutralButton.style.marginBottom = '5px';

rewriteNeutralButton.addEventListener('click', function() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        chrome.runtime.sendMessage({ action: 'rewrite_neutral', text: selectedText }, function(response) {
            if (response && response.rewrite) {
                const rewrittenText = response.rewrite;

                // Automatically copy the rewritten text to the clipboard
                navigator.clipboard.writeText(rewrittenText).then(function() {
                    alert('Rewritten Text (Neutral):\\n\\n' + rewrittenText + '\\n\\n(Copied to clipboard)');
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                    alert('Rewritten Text (Neutral):\\n\\n' + rewrittenText);
                });
            } else {
                alert('Failed to get rewrite: ' + (response.error || 'Unknown error.'));
            }
        });
    } else {
        alert('No text is highlighted.');
    }
});

const simplifyTextButton = document.createElement('button');
simplifyTextButton.textContent = 'Simplify English';
simplifyTextButton.style.padding = '5px 10px';
simplifyTextButton.style.fontSize = '14px';
simplifyTextButton.style.cursor = 'pointer';
simplifyTextButton.style.backgroundColor = '#28a745'; // Green
simplifyTextButton.style.color = 'white';
simplifyTextButton.style.border = 'none';
simplifyTextButton.style.borderRadius = '3px';
simplifyTextButton.style.marginBottom = '5px';

simplifyTextButton.addEventListener('click', function() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        chrome.runtime.sendMessage({ action: 'simplify_text', text: selectedText }, function(response) {
            if (response && response.simplified) {
                const simplifiedText = response.simplified;

                // Automatically copy the simplified text to the clipboard
                navigator.clipboard.writeText(simplifiedText).then(function() {
                    alert('Simplified Text:\\n\\n' + simplifiedText + '\\n\\n(Copied to clipboard)');
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                    alert('Simplified Text:\\n\\n' + simplifiedText);
                });
            } else {
                alert('Failed to simplify text: ' + (response.error || 'Unknown error.'));
            }
        });
    } else {
        alert('No text is highlighted.');
    }
});

const setApiKeyButton = document.createElement('button');
setApiKeyButton.textContent = 'Set OpenAI API Key';
setApiKeyButton.style.padding = '5px 10px';
setApiKeyButton.style.fontSize = '14px';
setApiKeyButton.style.cursor = 'pointer';
setApiKeyButton.style.backgroundColor = '#ffc107'; // Yellow
setApiKeyButton.style.color = 'black';
setApiKeyButton.style.border = 'none';
setApiKeyButton.style.borderRadius = '3px';
setApiKeyButton.style.marginTop = '5px';

setApiKeyButton.addEventListener('click', function() {
    const apiKey = prompt('Enter your OpenAI API Key:');
    if (apiKey) {
        chrome.storage.sync.set({ 'openai_api_key': apiKey }, function() {
            alert('API key saved successfully.');
        });
    }
});

guiContainer.appendChild(jumpToFilesButton);
guiContainer.appendChild(insertTextButton);
guiContainer.appendChild(rewritePositiveButton);
guiContainer.appendChild(rewriteNeutralButton);
guiContainer.appendChild(simplifyTextButton);
guiContainer.appendChild(setApiKeyButton);
document.body.appendChild(guiContainer);
'''

# background.js content with the updated "Simplify English" prompt
background_js_content = '''
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'rewrite_positive') {
        rewriteText(request.text, 'positive', sendResponse);
        return true; // Keep the message channel open for sendResponse
    }
    if (request.action === 'rewrite_neutral') {
        rewriteText(request.text, 'neutral', sendResponse);
        return true;
    }
    if (request.action === 'simplify_text') {
        simplifyText(request.text, sendResponse);
        return true;
    }
});

async function rewriteText(text, tone, sendResponse) {
    try {
        const apiKey = await getApiKey();
        if (!apiKey) {
            sendResponse({ error: 'API key not set. Please click "Set OpenAI API Key" and enter your API key.' });
            return;
        }

        const prompt = `Please rewrite the following text in a ${tone} tone while keeping all the original details:

Text:
"""${text}"""`;

        const data = await callOpenAiApi(prompt, apiKey);

        if (data.error) {
            console.error('API Error:', data.error);
            sendResponse({ error: data.error.message });
        } else {
            const rewrite = data.choices[0].message.content.trim();
            console.log('Rewrite obtained:', rewrite);
            sendResponse({ rewrite: rewrite });
        }
    } catch (error) {
        console.error('An error occurred during rewriting:', error);
        sendResponse({ error: 'An error occurred during rewriting.' });
    }
}

async function simplifyText(text, sendResponse) {
    try {
        const apiKey = await getApiKey();
        if (!apiKey) {
            sendResponse({ error: 'API key not set. Please click "Set OpenAI API Key" and enter your API key.' });
            return;
        }

        const prompt = `Please simplify the following text to make it brief and include direct action items. Retain main focal points as bullet points where appropriate, but also include some dialogue. Avoid making the entire text into bullet points. The goal is to keep all details and specifications, making the text straightforward and less conversational.

Text:
"""${text}"""`;

        const data = await callOpenAiApi(prompt, apiKey);

        if (data.error) {
            console.error('API Error:', data.error);
            sendResponse({ error: data.error.message });
        } else {
            const simplified = data.choices[0].message.content.trim();
            console.log('Simplified text obtained:', simplified);
            sendResponse({ simplified: simplified });
        }
    } catch (error) {
        console.error('An error occurred during text simplification:', error);
        sendResponse({ error: 'An error occurred during text simplification.' });
    }
}

function getApiKey() {
    return new Promise((resolve) => {
        chrome.storage.sync.get(['openai_api_key'], function(result) {
            resolve(result.openai_api_key);
        });
    });
}

function callOpenAiApi(prompt, apiKey) {
    return fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + apiKey
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: [{ "role": "user", "content": prompt }],
            max_tokens: 1000,
            n: 1,
            temperature: 0.5
        })
    }).then(response => response.json());
}
'''

# Write the manifest.json file
with open(os.path.join(project_dir, "manifest.json"), "w", encoding='utf-8') as manifest_file:
    manifest_file.write(manifest_content)

# Write the content.js file
with open(os.path.join(project_dir, "content.js"), "w", encoding='utf-8') as content_script_file:
    content_script_file.write(content_js_content)

# Write the background.js file
with open(os.path.join(project_dir, "background.js"), "w", encoding='utf-8') as background_script_file:
    background_script_file.write(background_js_content)

print(f"Chrome extension project generated in '{project_dir}' folder.")
print("Please follow these steps to set up and use the extension:")
print("1. Open Chrome and go to chrome://extensions/")
print("2. Enable 'Developer mode' in the top right corner.")
print(f"3. Click 'Load unpacked' and select the '{project_dir}' folder.")
print("4. On any webpage, click the 'Set OpenAI API Key' button in the GUI to enter your API key.")
