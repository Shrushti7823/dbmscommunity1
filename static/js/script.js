
  const branches = {
    "Computer Engineering": "computer-engineering",
    "Information Technology": "information-technology",
    "Artificial Intelligence and Data Science": "ai-ds",
    "Computer Science and Design": "computer-science-and-design",
    "Electronics & Telecommunication Engineering": "electronics-engineering",
    "Robotics and Automation Engineering": "robotics-engineering",
    "Electrical Engineering": "electrical-engineering",
    "Chemical Engineering": "chemical-engineering",
    "Mechanical Engineering": "mechanical-engineering",
    "Civil Engineering": "civil-engineering"
  };

  const searchInput = document.getElementById("searchInput");
  let lastSelected = "";

  searchInput.addEventListener("input", function () {
    const input = this.value.toLowerCase();
    closeSuggestions();
    if (!input) return;

    const matches = Object.keys(branches).filter(branch =>
      branch.toLowerCase().includes(input) &&
      branch.toLowerCase() !== lastSelected.toLowerCase()
    );

    if (matches.length === 0) return;

    const list = document.createElement("ul");
    list.setAttribute("id", "suggestions-list");
    Object.assign(list.style, {
      position: "absolute",
      backgroundColor: "#fff",
      border: "1px solid #ccc",
      listStyle: "none",
      padding: "5px",
      marginTop: "5px",
      width: `${searchInput.offsetWidth}px`,
      zIndex: "1000"
    });

    matches.forEach(branch => {
      const item = document.createElement("li");
      item.textContent = branch;
      Object.assign(item.style, {
        padding: "4px",
        cursor: "pointer"
      });
      item.addEventListener("click", function () {
        searchInput.value = branch;
        lastSelected = branch;
        closeSuggestions();

        const sectionId = branches[branch];
        const section = document.getElementById(sectionId);
        if (section) {
          section.scrollIntoView({ behavior: "smooth", block: "center" });

          // Remove old highlights
          document.querySelectorAll(".highlight-card").forEach(card => {
            card.classList.remove("highlight-card");
          });

          // Add highlight to the selected section
          section.querySelector(".card").classList.add("highlight-card");
        }
      });
      list.appendChild(item);
    });

    searchInput.parentNode.appendChild(list);
  });

  function closeSuggestions() {
    const oldList = document.getElementById("suggestions-list");
    if (oldList) oldList.remove();
  }


