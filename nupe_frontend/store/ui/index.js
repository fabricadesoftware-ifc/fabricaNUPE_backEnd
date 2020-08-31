export const state = () => ({
  isFooterBarVisible: true,
  isNavBarVisible: true,
  isAsideMobileExpanded: false,
  isAsideVisible: true,
  userName: "Eduardo"
});

export const mutations = {
  setAsideVisible(state, value) {
    state.isAsideVisible = value;
  }
};

export const actions = {
  noAsideVisible({ commit }) {
    commit("setAsideVisible", false);
  },

  asideVisible({ commit }) {
    commit("setAsideVisible", true);
  }
};
