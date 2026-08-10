const searchInput = document.querySelector("#search");
const difficultyFilter = document.querySelector("#difficulty-filter");
const sceneFilter = document.querySelector("#scene-filter");
const resultCount = document.querySelector("#vocabulary-result-count");
const emptyState = document.querySelector("#vocabulary-empty");
const rows = [...document.querySelectorAll("#vocabulary-table tbody tr")];
const total = rows.length;

function filterRows() {
  const query = searchInput.value.trim().toLowerCase();
  const difficulty = difficultyFilter.value;
  const scene = sceneFilter.value;
  let visible = 0;

  rows.forEach((row) => {
    const matchesSearch =
      !query || row.dataset.search.includes(query);

    const matchesDifficulty =
      !difficulty || row.dataset.difficulty === difficulty;

    const matchesScene =
      !scene || row.dataset.scene === scene;

    const show = matchesSearch && matchesDifficulty && matchesScene;
    row.hidden = !show;
    if (show) visible += 1;
  });

  resultCount.textContent =
    visible === total
      ? `${total} terms`
      : `${visible} of ${total} terms`;

  emptyState.hidden = visible > 0;
}

searchInput.addEventListener("input", filterRows);
difficultyFilter.addEventListener("change", filterRows);
sceneFilter.addEventListener("change", filterRows);

filterRows();
