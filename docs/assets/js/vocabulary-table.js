const searchInput = document.querySelector("#search");
const difficultyFilter = document.querySelector("#difficulty-filter");
const sceneFilter = document.querySelector("#scene-filter");
const rows = [...document.querySelectorAll("#vocabulary-table tbody tr")];

function filterRows() {
  const query = searchInput.value.trim().toLowerCase();
  const difficulty = difficultyFilter.value;
  const scene = sceneFilter.value;

  rows.forEach((row) => {
    const matchesSearch =
      !query || row.dataset.search.includes(query);

    const matchesDifficulty =
      !difficulty || row.dataset.difficulty === difficulty;

    const matchesScene =
      !scene || row.dataset.scene === scene;

    row.hidden = !(
      matchesSearch &&
      matchesDifficulty &&
      matchesScene
    );
  });
}

searchInput.addEventListener("input", filterRows);
difficultyFilter.addEventListener("change", filterRows);
sceneFilter.addEventListener("change", filterRows);
