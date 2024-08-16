import math

import pandas as pd

from ..decorator import block


@block(block_name="process_stochastics", series_required_columns=["close", "low", "high"])
class ProcessStochasticsBlock:
    series: pd.DataFrame

    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df_ = df.copy()
        df_["K"] = self._fast_stochastic_k(df_["close"], df_["low"], df_["high"], 9)
        df_["D"] = self._fast_stochastic_d(df_["K"])
        df_["SD"] = self._slow_stochastic_d(df_["D"])
        return df_

    def _signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        買いと売りに関する指標を算出する
        """
        df = df.assign(
            shift_K=lambda x: x["K"].shift(1),
            shift_D=lambda x: x["D"].shift(1),
            shift_SD=lambda x: x["SD"].shift(1),
        ).fillna(0)

        # 複数引数は関数を利用することで吸収
        df["stochastics_buy_signal"] = df.apply(self._buy_signal_index_internal, axis=1)
        df["stochastics_sell_signal"] = df.apply(self._sell_signal_index_internal, axis=1)
        return df

    @staticmethod
    def _fast_stochastic_k(close, low, high, n):
        return (
            (close - low.rolling(window=n, center=False).min())
            / (high.rolling(window=n, center=False).max() - low.rolling(window=n, center=False).min())
        ) * 100

    @staticmethod
    def _fast_stochastic_d(stochastic_k):
        # ストキャスの%Dを計算（%Kの3日SMA）
        return stochastic_k.rolling(window=3, center=False).mean()

    @staticmethod
    def _slow_stochastic_d(stochastic_d):
        # ストキャスの%SDを計算（%Dの3日SMA）
        return stochastic_d.rolling(window=3, center=False).mean()

    @staticmethod
    def _buy_signal_index_internal(x: pd.Series) -> float:
        return ProcessStochasticsBlock._buy_signal_index(
            x["K"], x["D"], x["SD"], x["shift_K"], x["shift_D"], x["shift_SD"]
        )

    @staticmethod
    def _buy_signal_index(current_k, current_d, current_sd, prev_k, prev_d, prev_sd) -> float:
        if (current_k > 30) | (current_d > 30) | (current_sd > 30):
            return 0

        # %K・%D共に20％以下の時に、%Kが%Dを下から上抜いた時
        if current_k < 20 and current_d < 20:
            if (prev_d > prev_k) and (current_d < current_k):
                return current_k - current_d

        # %D・スロー%D共に20％以下の時に、%Dがスロー%Dを下から上抜いた時
        if current_d < 20 and current_sd < 20:
            if (prev_sd > prev_d) and (current_sd < current_d):
                return current_d - current_sd
        return 1 / math.exp(
            math.pow(current_k - 20, 2) / 100 + math.pow(current_d - 20, 2) / 100 + math.pow(current_sd - 20, 2) / 100
        )

    @staticmethod
    def _sell_signal_index_internal(x: pd.Series) -> float:
        return ProcessStochasticsBlock._sell_signal_index(
            x["K"], x["D"], x["SD"], x["shift_K"], x["shift_D"], x["shift_SD"]
        )

    @staticmethod
    def _sell_signal_index(current_k, current_d, current_sd, prev_k, prev_d, prev_sd) -> float:
        if (current_k < 70) | (current_d < 70) | (current_sd < 70):
            return 0

        # %K・%D共に80％以上の時に、%Kが%Dを上から下抜いた時
        if current_k > 80 and current_d > 80:
            if (prev_d < prev_k) and (current_d > current_k):
                return current_d - current_k

        # %D・スロー%D共に80％以上の時に、%Dがスロー%Dを上から下抜いた時
        # %D・スロー%D共に20％以下の時に、%Dがスロー%Dを下から上抜いた時
        if current_d > 80 and current_sd > 80:
            if (prev_sd < prev_d) and (current_sd > current_d):
                return current_d - current_sd
        return 1 / math.exp(
            math.pow(current_k - 20, 2) / 100 + math.pow(current_d - 20, 2) / 100 + math.pow(current_sd - 20, 2) / 100
        )

    def _process(self) -> pd.DataFrame:
        applied_df = self._apply(df=self.series)
        signal_df = self._signal(df=applied_df)
        required_columns = ["K", "D", "SD", "stochastics_buy_signal", "stochastics_sell_signal"]
        return signal_df[required_columns]
