<script lang="ts">
  import "../app.css";
  import Profile from "../icons/Profile.svelte";
  import Home from "../icons/Home.svelte";

  let { children } = $props();
</script>

<nav
  class="top-0 flex w-full items-center justify-between bg-lilac px-5 pb-2 pt-1 text-2xl text-white"
>
  <div>
    <img src="/logo.gif" alt="Logo" class="w-32" />
  </div>
  <div class="justify-between">
    <ul class="justify-space-between flex flex-wrap gap-4">
      <li>
        <a href="/" class="hover:text-sky-200 hover:underline">
          <Home />
        </a>
      </li>
      <li>
        <a href="/profile" class="hover:text-sky-200 hover:underline">
          <Profile />
        </a>
      </li>
    </ul>
  </div>
</nav>

{@render children()}
