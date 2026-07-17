const analyzeBtn = document.getElementById("analyzeBtn");

const ticket = document.getElementById("ticket");

const ticketSelect = document.getElementById("ticketSelect");
const loadTicket = document.getElementById("loadTicket");

const category = document.getElementById("category");
const urgency = document.getElementById("urgency");
const confidence = document.getElementById("confidence");
const tools = document.getElementById("tools");

const customerName = document.getElementById("customerName");
const customerEmail = document.getElementById("customerEmail");
const customerIssue = document.getElementById("customerIssue");

const orderId = document.getElementById("orderId");
const orderStatus = document.getElementById("orderStatus");
const refundStatus = document.getElementById("refundStatus");

const timeline = document.getElementById("timeline");

const emailCard = document.getElementById("emailCard");



let lastResult = null;

// =============================
// Analyze Ticket
// =============================

analyzeBtn.addEventListener("click", analyzeTicket);

    async function analyzeTicket() {

     if (ticket.value.trim() === "") {

        alert("Please enter a customer ticket.");

        return;
    }
    
    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "Analyzing...";
    const loadingPromise = showLoading();
    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                ticket: ticket.value

            })

        });

        const data = await response.json();
        await loadingPromise;


    document
        .getElementById(
        "loadingScreen"
        );

console.log(
    "ANALYZE DATA:",
    data
);
        if (data.approval_required) {

            document
                .getElementById(
                    "loadingScreen"
                )
                .classList.add(
                    "hidden"
                );

            showApprovalModal(
                data
            );

            return;
        }

        lastResult = data;

        displayResult(data);

        document
    .getElementById("loadingScreen")
    .classList.add("hidden");

    }

    catch (err) {

    document
        .getElementById(
            "loadingScreen"
        )
        .classList.add(
            "hidden"
        );

    alert(
        "Unable to contact server."
    );

    console.error(err);

    }
    finally{
            
            analyzeBtn.disabled = false;

            analyzeBtn.innerText =
             "Analyze Ticket";
    }
}

// =============================
// Display Results
// =============================

function displayResult(data) {

    category.textContent =
        data.classification.category;

    urgency.textContent =
        data.classification.urgency;

    confidence.textContent =
        Math.round(data.classification.confidence * 100) + "%";

    tools.textContent =
        data.plan.tools.join(", ");


    // Customer

    customerName.textContent =
        data.extraction.customer_name || "-";

    customerEmail.textContent =
        data.extraction.email || "-";

    customerIssue.textContent =
        data.extraction.issue || "-";


    // Order

    orderId.textContent =
        data.extraction.order_id || "-";

    orderStatus.textContent = "-";
    refundStatus.textContent = "-";

    timeline.innerHTML = "";


    // Timeline

    addTimeline("📨", "Ticket received");

    addTimeline("🧠", "AI classified ticket");

    addTimeline("📋", "Information extracted");

    addTimeline("🛠️", "Execution plan created");


    data.tool_results.forEach(item => {

        if (item.tool === "lookup_order_status") {

            orderStatus.textContent =
                item.result.status;

            addTimeline(
                "📦",
                "Order status checked"
            );
        }

        if (item.tool === "lookup_customer") {

            addTimeline(
                "👤",
                "Customer profile loaded"
            );
        }

        if (item.tool === "issue_refund") {

            if (item.result.success) {

                refundStatus.textContent =
                    "Processed";

                addTimeline(
                    "✅",
                    "Refund processed successfully"
                );

            } else {

                refundStatus.textContent =
                    "Pending Approval";

                addTimeline(
                    "⚠️",
                    "Refund awaiting approval"
                );

            }

        }

    });


    if (data.context) {

        addTimeline(
            "📚",
            "Knowledge Base consulted"
        );

    }


    addTimeline(
        "✉️",
        "Email drafted"
    );


    emailCard.innerHTML = `

        <strong>${data.email.subject}</strong>

        <hr style="margin:20px 0; border:none; border-top:1px solid #e5e7eb;">

        ${data.email.body.replace(/\n/g,"<br>")}

    `;

}



function addTimeline(icon,text){

    timeline.innerHTML += `

        <div class="timeline-item">

            <div class="timeline-icon">

                ${icon}

            </div>

            <div class="timeline-text">

                ${text}

            </div>

        </div>

    `;

}



// =============================
// Demo Tickets
// =============================

let demoTickets = [];

loadDemoTickets();

async function loadDemoTickets() {

    const response = await fetch("/sample-tickets");

    demoTickets = await response.json();

    demoTickets.forEach(ticket => {

        ticketSelect.innerHTML += `
            <option value="${ticket.id}">
                ${ticket.title} • ${ticket.scenario}
            </option>
        `;

    });

}

loadTicket.addEventListener("click", () => {

    const id = Number(ticketSelect.value);

    const selected = demoTickets.find(
        t => t.id === id
    );

    if (!selected)
        return;

    ticket.value = selected.ticket;

});

const modal =
    document.getElementById("approvalModal");

const approvalReason =
    document.getElementById("approvalReason");

const approveBtn =
    document.getElementById("approveBtn");

const rejectBtn =
    document.getElementById("rejectBtn");

function formatTool(tool){

    const names={

        issue_refund:
            "Process Customer Refund",

        cancel_order:
            "Cancel Customer Order",

        escalate_to_human:
            "Escalate to Human Support",

        human_review:
            "Supervisor Review"
    };

    return names[tool] || tool;
}


function showApprovalModal(data){

    approvalReason.innerHTML = `

        <strong>Action:</strong>
        ${formatTool(data.tool)}

        <br><br>

        <strong>Reason:</strong>
        ${data.reason}

    `;

    modal.classList.remove("hidden");

    approveBtn.onclick = async () => {
        showLoading();
        const response =
            await fetch("/approve",{
                method:"POST"
            });

        const result =
            await response.json();

        document
            .getElementById(
                "loadingScreen"
            )
            .classList.add(
                "hidden"
            );  

        modal.classList.add("hidden");

        lastResult=result;

        displayResult(result);

    };

    rejectBtn.onclick = async ()=>{

        await fetch("/reject",{
            method:"POST"
        });

        modal.classList.add("hidden");

    };

}

const steps = [

    "Reading Ticket",
    "Understanding Context",
    "Extracting Customer Data",
    "Looking Up Orders",
    "Reviewing Company Policies",
    "Drafting Email",
    "Finalizing Response"
];
async function showLoading() {

    document
        .getElementById("loadingScreen")
        .classList.remove("hidden");

    const timeline =
        document.getElementById("loadingTimeline");

    timeline.innerHTML = "";

    for (const step of steps) {

        timeline.innerHTML += `
            <div class="timeline-step">
                <div class="circle"></div>
                <span>${step}</span>
            </div>
        `;

        await new Promise(
            r => setTimeout(r, 700)
        );
    }
}