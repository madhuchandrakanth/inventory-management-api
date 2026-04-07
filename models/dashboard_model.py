from pydantic import BaseModel


class Dashboard(BaseModel):
    summary: list
    revenueAndProfit: dict


class Summary(BaseModel):
    title: str
    value: str
    trend: str
    trendText: str
    isPositive: bool


class RevenueAndProfit(BaseModel):
    labels: list
    datasets: list


class Dataset(BaseModel):
    label: str
    data: list
