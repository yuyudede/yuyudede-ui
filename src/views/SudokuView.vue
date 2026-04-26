<template>
  <div class="sudoku-page">
    <div class="sudoku-container">
      <!-- Header -->
      <div class="sudoku-header">
        <div class="header-left">
          <router-link to="/tools" class="back-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
            <span>工具箱</span>
          </router-link>
          <h1 class="game-title">数独</h1>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>{{ formatTime(timer) }}</span>
          </div>
          <div class="stat-item mistakes" v-if="mistakes > 0">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            <span>{{ mistakes }}/3</span>
          </div>
        </div>
      </div>

      <!-- Difficulty selector -->
      <div class="difficulty-bar">
        <button
          v-for="d in difficulties"
          :key="d.value"
          class="diff-btn"
          :class="{ active: difficulty === d.value }"
          @click="changeDifficulty(d.value)"
        >{{ d.label }}</button>
      </div>

      <!-- Board -->
      <div class="board-wrapper">
        <div class="board" :class="{ paused: isPaused }">
          <template v-for="(row, r) in board" :key="r">
            <div
              v-for="(cell, c) in row"
              :key="`${r}-${c}`"
              class="cell"
              :class="cellClasses(r, c)"
              @click="selectCell(r, c)"
            >
              <span v-if="cell !== 0">{{ cell }}</span>
            </div>
          </template>
        </div>
        <!-- Pause overlay -->
        <div v-if="isPaused" class="pause-overlay" @click="togglePause">
          <div class="pause-text">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
            <span>已暂停</span>
          </div>
        </div>
      </div>

      <!-- Controls -->
      <div class="controls">
        <button class="ctrl-btn erase" @click="eraseCell" :disabled="!selected">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/><line x1="18" y1="9" x2="12" y2="15"/><line x1="12" y1="9" x2="18" y2="15"/></svg>
          <span>擦除</span>
        </button>
        <button class="ctrl-btn pause" @click="togglePause">
          <svg v-if="isPaused" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
          <span>{{ isPaused ? '继续' : '暂停' }}</span>
        </button>
        <button class="ctrl-btn undo" @click="undo" :disabled="history.length === 0">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          <span>撤销</span>
        </button>
        <button class="ctrl-btn new-game" @click="newGame">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
          <span>新游戏</span>
        </button>
      </div>

      <!-- Number pad -->
      <div class="numpad">
        <button
          v-for="n in 9"
          :key="n"
          class="num-btn"
          :class="{ completed: isNumberComplete(n) }"
          @click="inputNumber(n)"
        >{{ n }}</button>
      </div>
    </div>

    <!-- Victory Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="showVictory" class="victory-overlay" @click.self="showVictory = false">
          <div class="victory-card">
            <div class="victory-emoji">🎉</div>
            <h2>恭喜通关!</h2>
            <div class="victory-stats">
              <div class="v-stat">
                <span class="v-label">难度</span>
                <span class="v-value">{{ difficultyLabel }}</span>
              </div>
              <div class="v-stat">
                <span class="v-label">用时</span>
                <span class="v-value">{{ formatTime(timer) }}</span>
              </div>
              <div class="v-stat">
                <span class="v-label">错误</span>
                <span class="v-value">{{ mistakes }} 次</span>
              </div>
            </div>
            <button class="victory-btn" @click="newGame(); showVictory = false">再来一局</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onBeforeUnmount, watch } from 'vue'
import { useHead } from '@unhead/vue'

useHead({
  title: '数独 - 工具箱',
})

// ==================== Game State ====================
const board = reactive(Array(9).fill(null).map(() => Array(9).fill(0)))
const solution = reactive(Array(9).fill(null).map(() => Array(9).fill(0)))
const initial = reactive(Array(9).fill(null).map(() => Array(9).fill(false)))
const selected = ref(null)
const conflicts = ref(new Set())
const mistakes = ref(0)
const timer = ref(0)
const isPaused = ref(false)
const showVictory = ref(false)
const difficulty = ref('medium')
const history = ref([])
let timerInterval = null

const difficulties = [
  { value: 'easy', label: '简单', remove: 38 },
  { value: 'medium', label: '中等', remove: 45 },
  { value: 'hard', label: '困难', remove: 52 },
  { value: 'expert', label: '专家', remove: 56 },
]

const difficultyLabel = computed(() => {
  return difficulties.find(d => d.value === difficulty.value)?.label || ''
})

// ==================== Algorithm ====================
function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function isValidPlacement(boardArr, row, col, num) {
  for (let i = 0; i < 9; i++) {
    if (boardArr[row][i] === num) return false
    if (boardArr[i][col] === num) return false
  }
  const boxR = Math.floor(row / 3) * 3
  const boxC = Math.floor(col / 3) * 3
  for (let r = boxR; r < boxR + 3; r++) {
    for (let c = boxC; c < boxC + 3; c++) {
      if (boardArr[r][c] === num) return false
    }
  }
  return true
}

function solveBoard(boardArr) {
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (boardArr[r][c] === 0) {
        for (let num = 1; num <= 9; num++) {
          if (isValidPlacement(boardArr, r, c, num)) {
            boardArr[r][c] = num
            if (solveBoard(boardArr)) return true
            boardArr[r][c] = 0
          }
        }
        return false
      }
    }
  }
  return true
}

function generatePuzzle() {
  // Step 1: Fill diagonal 3x3 boxes
  const b = Array(9).fill(null).map(() => Array(9).fill(0))
  for (let box = 0; box < 9; box += 3) {
    const nums = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])
    let idx = 0
    for (let r = box; r < box + 3; r++) {
      for (let c = box; c < box + 3; c++) {
        b[r][c] = nums[idx++]
      }
    }
  }

  // Step 2: Solve the board
  const sol = b.map(row => [...row])
  solveBoard(sol)

  // Step 3: Copy solution
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      solution[r][c] = 0
    }
  }

  // Step 4: Create puzzle by removing cells
  const puzzle = sol.map(row => [...row])
  const removeCount = difficulties.find(d => d.value === difficulty.value)?.remove || 45
  const cells = shuffle(
    Array.from({ length: 81 }, (_, i) => [Math.floor(i / 9), i % 9])
  ).slice(0, removeCount)

  for (const [r, c] of cells) {
    puzzle[r][c] = 0
  }

  // Apply to reactive arrays
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      board[r][c] = puzzle[r][c]
      solution[r][c] = sol[r][c]
      initial[r][c] = puzzle[r][c] !== 0
    }
  }
}

// ==================== Timer ====================
function startTimer() {
  stopTimer()
  timer.value = 0
  timerInterval = setInterval(() => {
    if (!isPaused.value) {
      timer.value++
    }
  }, 1000)
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

// ==================== Game Actions ====================
function selectCell(r, c) {
  if (isPaused.value) return
  if (initial[r][c]) return
  selected.value = { row: r, col: c }
}

function inputNumber(num) {
  if (!selected.value || isPaused.value) return
  const { row, col } = selected.value
  if (initial[row][col]) return

  history.value.push({ row, col, prev: board[row][col] })

  if (board[row][col] === num) {
    board[row][col] = 0
  } else {
    board[row][col] = num
    // Check conflict
    checkConflicts()
    if (num !== solution[row][col]) {
      mistakes.value++
      if (mistakes.value >= 3) {
        isPaused.value = true
        // Reveal all wrong cells
        setTimeout(() => {
          alert('已错误 3 次，游戏结束。请开始新游戏。')
        }, 100)
      }
    }
  }
  checkVictory()
}

function eraseCell() {
  if (!selected.value || isPaused.value) return
  const { row, col } = selected.value
  if (initial[row][col]) return
  if (board[row][col] === 0) return
  history.value.push({ row, col, prev: board[row][col] })
  board[row][col] = 0
  checkConflicts()
}

function undo() {
  if (history.value.length === 0 || isPaused.value) return
  const last = history.value.pop()
  board[last.row][last.col] = last.prev
  checkConflicts()
}

function togglePause() {
  isPaused.value = !isPaused.value
}

function changeDifficulty(d) {
  difficulty.value = d
  newGame()
}

function newGame() {
  stopTimer()
  board.length = 0
  solution.length = 0
  initial.length = 0
  for (let i = 0; i < 9; i++) {
    board.push(Array(9).fill(0))
    solution.push(Array(9).fill(0))
    initial.push(Array(9).fill(false))
  }
  selected.value = null
  conflicts.value = new Set()
  mistakes.value = 0
  isPaused.value = false
  showVictory.value = false
  history.value = []
  generatePuzzle()
  startTimer()
}

function checkConflicts() {
  const cSet = new Set()
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (board[r][c] === 0) continue
      // Check row
      for (let k = 0; k < 9; k++) {
        if (k !== c && board[r][k] === board[r][c]) {
          cSet.add(`${r},${c}`)
          cSet.add(`${r},${k}`)
        }
      }
      // Check col
      for (let k = 0; k < 9; k++) {
        if (k !== r && board[k][c] === board[r][c]) {
          cSet.add(`${r},${c}`)
          cSet.add(`${k},${c}`)
        }
      }
      // Check box
      const boxR = Math.floor(r / 3) * 3
      const boxC = Math.floor(c / 3) * 3
      for (let rr = boxR; rr < boxR + 3; rr++) {
        for (let cc = boxC; cc < boxC + 3; cc++) {
          if ((rr !== r || cc !== c) && board[rr][cc] === board[r][c]) {
            cSet.add(`${r},${c}`)
            cSet.add(`${rr},${cc}`)
          }
        }
      }
    }
  }
  conflicts.value = cSet
}

function checkVictory() {
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (board[r][c] !== solution[r][c]) return
    }
  }
  stopTimer()
  showVictory.value = true
}

function isNumberComplete(n) {
  const count = board.flat().filter(v => v === n).length
  return count === 9
}

function cellClasses(r, c) {
  if (!selected.value) return {}
  const { row, col } = selected.value
  const key = `${r},${c}`
  return {
    selected: r === row && c === col,
    same: board[r][c] !== 0 && board[r][c] === board[row][col] && (r !== row || c !== col),
    related: r === row || c === col || (Math.floor(r / 3) === Math.floor(row / 3) && Math.floor(c / 3) === Math.floor(col / 3)),
    conflict: conflicts.value.has(key) && board[r][c] !== 0,
    initial: initial[r][c],
    wrong: board[r][c] !== 0 && board[r][c] !== solution[r][c] && !initial[r][c],
  }
}

// ==================== Keyboard ====================
function onKeydown(e) {
  if (isPaused.value && e.key !== 'Escape') return

  if (e.key === 'Escape') {
    if (isPaused.value) {
      isPaused.value = false
    } else {
      selected.value = null
    }
    return
  }

  if (e.key === 'p' || e.key === 'P') {
    togglePause()
    return
  }

  if (e.key === 'z' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault()
    undo()
    return
  }

  // Arrow keys
  if (selected.value && ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
    e.preventDefault()
    let { row, col } = selected.value
    if (e.key === 'ArrowUp') row = (row + 8) % 9
    if (e.key === 'ArrowDown') row = (row + 1) % 9
    if (e.key === 'ArrowLeft') col = (col + 8) % 9
    if (e.key === 'ArrowRight') col = (col + 1) % 9
    selected.value = { row, col }
    return
  }

  // Number keys
  const num = parseInt(e.key)
  if (num >= 1 && num <= 9) {
    inputNumber(num)
    return
  }

  // Delete/Backspace
  if (e.key === 'Backspace' || e.key === 'Delete') {
    eraseCell()
    return
  }
}

// ==================== Lifecycle ====================
newGame()

window.addEventListener('keydown', onKeydown)

onBeforeUnmount(() => {
  stopTimer()
  window.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.sudoku-page {
  max-width: 520px;
  margin: 0 auto;
  padding: 24px 20px 60px;
  min-height: calc(100vh - 64px);
}

.sudoku-container {
  animation: fadeUp 0.5s cubic-bezier(0.2,0.8,0.2,1);
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.sudoku-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85rem;
  transition: color 0.2s;
  padding: 4px 8px;
  border-radius: 6px;
}
.back-btn:hover {
  color: var(--primary);
  background: rgba(129,140,248,0.08);
}
.game-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-primary);
}
.header-stats {
  display: flex;
  gap: 14px;
}
.stat-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.88rem;
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
}
.stat-item.mistakes {
  color: #ef4444;
}

/* Difficulty */
.difficulty-bar {
  display: flex;
  gap: 6px;
  margin-bottom: 20px;
  background: var(--bg-surface);
  border-radius: 12px;
  padding: 4px;
  border: 1px solid var(--border-color);
}
.diff-btn {
  flex: 1;
  padding: 7px 0;
  border: none;
  border-radius: 9px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
  font-family: inherit;
}
.diff-btn:hover {
  color: var(--text-primary);
}
.diff-btn.active {
  background: linear-gradient(135deg, #818cf8, #a78bfa);
  color: #fff;
  box-shadow: 0 2px 8px rgba(129,140,248,0.3);
}

/* Board */
.board-wrapper {
  position: relative;
  margin-bottom: 20px;
}
.board {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  grid-template-rows: repeat(9, 1fr);
  aspect-ratio: 1;
  border: 2.5px solid var(--text-primary);
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-surface);
  transition: filter 0.3s;
}
.board.paused {
  filter: blur(6px);
  pointer-events: none;
}

.cell {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(1.2rem, 4.5vw, 1.55rem);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  user-select: none;
  border-right: 1px solid var(--border-soft);
  border-bottom: 1px solid var(--border-soft);
  transition: background 0.15s, color 0.15s;
  position: relative;
  color: var(--primary);
}

.cell.initial {
  color: var(--text-primary);
}

/* 3x3 thick borders */
.cell:nth-child(3n) {
  border-right: 2.5px solid var(--text-primary);
}
.cell:nth-child(9n) {
  border-right: none;
}
.board .cell:nth-child(n+19):nth-child(-n+27),
.board .cell:nth-child(n+46):nth-child(-n+54) {
  border-bottom: 2.5px solid var(--text-primary);
}
.board .cell:nth-child(n+73):nth-child(-n+81) {
  border-bottom: none;
}

/* Cell states */
.cell.related {
  background: rgba(129,140,248,0.06);
}
.cell.selected {
  background: rgba(129,140,248,0.22) !important;
  box-shadow: inset 0 0 0 2px #818cf8;
}
.cell.same {
  background: rgba(129,140,248,0.13);
  color: #818cf8;
}
.cell.conflict {
  background: rgba(239,68,68,0.12) !important;
  color: #ef4444 !important;
}
.cell.wrong {
  color: #ef4444;
}
.cell:hover:not(.selected) {
  background: rgba(129,140,248,0.04);
}
:global(html.dark) .cell.related {
  background: rgba(129,140,248,0.08);
}
:global(html.dark) .cell.same {
  background: rgba(129,140,248,0.16);
}
:global(html.dark) .cell.selected {
  background: rgba(129,140,248,0.25) !important;
}

/* Pause overlay */
.pause-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: 8px;
  cursor: pointer;
  z-index: 2;
}
:global(html.dark) .pause-overlay {
  background: rgba(13,17,23,0.5);
}
.pause-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

/* Controls */
.controls {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}
.ctrl-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.ctrl-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
  background: rgba(129,140,248,0.04);
}
.ctrl-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.ctrl-btn.new-game {
  color: #fff;
  background: linear-gradient(135deg, #818cf8, #a78bfa);
  border: none;
  font-weight: 600;
}
.ctrl-btn.new-game:hover {
  box-shadow: 0 4px 16px rgba(129,140,248,0.35);
  transform: translateY(-1px);
}

/* Number pad */
.numpad {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 6px;
}
.num-btn {
  aspect-ratio: 1;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 1.2rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.num-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: rgba(129,140,248,0.04);
  transform: translateY(-1px);
}
.num-btn:active {
  transform: scale(0.95);
}
.num-btn.completed {
  opacity: 0.3;
  pointer-events: none;
}

/* Victory modal */
.victory-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15,23,42,0.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.victory-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 36px 32px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(15,23,42,0.2);
  min-width: 300px;
  animation: popIn 0.4s cubic-bezier(0.3,1.6,0.5,1);
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.85) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.victory-emoji {
  font-size: 3rem;
  margin-bottom: 8px;
}
.victory-card h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: var(--text-primary);
}
.victory-stats {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 24px;
}
.v-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.v-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.v-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}
.victory-btn {
  padding: 12px 36px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #818cf8, #ec4899);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
  font-family: inherit;
}
.victory-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(129,140,248,0.4);
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

/* Dark mode tweaks */
:global(html.dark) .board {
  border-color: var(--border-color);
}
:global(html.dark) .cell:nth-child(3n) {
  border-right-color: var(--border-color);
}
:global(html.dark) .board .cell:nth-child(n+19):nth-child(-n+27),
:global(html.dark) .board .cell:nth-child(n+46):nth-child(-n+54) {
  border-bottom-color: var(--border-color);
}

@media (max-width: 480px) {
  .sudoku-page {
    padding: 16px 12px 40px;
  }
  .controls {
    gap: 4px;
  }
  .ctrl-btn {
    padding: 8px 4px;
    font-size: 0.8rem;
    gap: 3px;
  }
  .numpad {
    gap: 4px;
  }
  .num-btn {
    font-size: 1rem;
    border-radius: 8px;
  }
}
</style>
