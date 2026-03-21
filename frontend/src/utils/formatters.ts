export function formatPercent(value: number, decimals: number = 1): string { return `${value.toFixed(decimals)}%`; }
export function formatTime(timestamp: number): string { return new Date(timestamp * 1000).toLocaleTimeString('pt-BR'); }
export function formatDateTime(timestamp: number): string { return new Date(timestamp * 1000).toLocaleString('pt-BR'); }
export function formatBytes(bytes: number, decimals: number = 2): string { if (bytes === 0) return '0 Bytes'; const k = 1024; const dm = decimals < 0 ? 0 : decimals; const sizes = ['Bytes', 'KB', 'MB', 'GB']; const i = Math.floor(Math.log(bytes) / Math.log(k)); return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`; }
export function truncateText(text: string, maxLength: number): string { return text.length <= maxLength ? text : `${text.slice(0, maxLength)}...`; }
export function capitalize(str: string): string { return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase(); }
export function formatDuration(seconds: number): string { const hours = Math.floor(seconds / 3600); const minutes = Math.floor((seconds % 3600) / 60); const secs = Math.floor(seconds % 60); const parts: string[] = []; if (hours > 0) parts.push(`${hours}h`); if (minutes > 0) parts.push(`${minutes}m`); if (secs > 0 || parts.length === 0) parts.push(`${secs}s`); return parts.join(' '); }
export function getResultColor(result: string): string { if (result === 'BANKER') return 'text-banker'; if (result === 'PLAYER') return 'text-player'; if (result === 'TIE') return 'text-tie'; return 'text-gray-500'; }
export function getResultEmoji(result: string): string { if (result === 'BANKER') return '🔴'; if (result === 'PLAYER') return '🔵'; if (result === 'TIE') return '🟡'; return '⚪'; }
