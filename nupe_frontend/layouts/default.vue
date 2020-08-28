<template>
  <div>
    <nav-bar />
    <aside-menu :menu="menu" />
    <nuxt />
    <footer-bar />
  </div>
</template>

<script>
import NavBar from "@/components/templates/NavBar";
import AsideMenu from "@/components/templates/AsideMenu";
import FooterBar from "@/components/templates/FooterBar";
import { mapActions } from "vuex";
export default {
  components: { NavBar, AsideMenu, FooterBar },
  computed: {
    menu() {
      return [
        "General",
        [
          {
            to: "/",
            icon: "desktop-mac",
            label: "Dashboard"
          }
        ],
        "Administração",
        [
          // {
          //   to: { name: "category" },
          //   label: this.$t("asideMenu.adminItems.category"),
          //   icon: "alpha-c-circle-outline"
          // },
          // {
          //   to: { name: "breed" },
          //   label: this.$t("asideMenu.adminItems.breed"),
          //   icon: "puzzle"
          // },
          // {
          //   label: this.$t("asideMenu.adminItems.sheep"),
          //   icon: "sheep",
          //   to: { name: "sheep" }
          // },
          // {
          //   label: this.$t("asideMenu.adminItems.records"),
          //   icon: "view-list",
          //   updateMark: true,
          //   menu: [
          //     {
          //       label: this.$t("asideMenu.adminItems.pregnancyDiagnosis"),
          //       icon: "medical-bag",
          //       to: { name: "pregnancyDiagnosis" }
          //     },
          //     {
          //       label: this.$t("asideMenu.adminItems.birth"),
          //       icon: "lightbulb-outline",
          //       to: { name: "birth" }
          //     }
          //   ]
          // }
        ],
        "About",
        [
          {
            href: "https://fabricadesoftware.ifc.edu.br",
            label: "About",
            icon: "help-circle"
          }
        ]
      ];
    }
  },

  created() {
    this.asideVisible();
  },
  methods: {
    ...mapActions("ui", ["asideVisible"])
  }
};
</script>

<style></style>
