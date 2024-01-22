def calculate_bootstrap(self, x: pd.DataFrame, y=None, n_bootstrap: int = 1000, n_cores: int = 1) -> pd.DataFrame:
        # bootstrap_res = list()
        option_dfs = list()
        for _ in range(n_bootstrap):
            bootstrap_df = x.copy()
            bootstrap_df.loc[:, self.event_date_col] = x[self.event_date_col].sample(frac=1).tolist()
            option_dfs.append(bootstrap_df.copy())

        bootstrap_res_list = run_in_parallel(
            func=self.run_study, 
            data=option_dfs, 
            n_cores=n_cores
        )
        bootstrap_df = pd.concat([
            calculate_car_stats(bootstrap_res_list[i])[['mean']].rename({'mean': i}, axis=1).copy() 
            for i in range(n_bootstrap)], axis=1)
        print('here2')
        return bootstrap_df
