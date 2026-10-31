<template>
	<AppShell />
</template>

<script setup>
// AppShell owns the regular workspace view; the dev-only demo route runs
// standalone so first-run gates and account APIs cannot block the preview.
import AppShell from "@/components/shell/AppShell.vue";
</script>
