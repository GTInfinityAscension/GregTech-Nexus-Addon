# 物品特效

GTNA 的终局材料拥有动态图标：光环、发光轮廓和三种着色器。这些特效由 GTNA 自行绘制；自 0.5.6 起不再需要 RenderBlender。

| 特效 | 外观 | 显示位置 |
|---|---|---|
| 光环 | 图标后方柔和的彩色圆盘 | 物品栏 |
| 发光边缘 | 图标后方一个着色、略大的图标副本 | 物品栏 |
| Cosmic（宇宙） | 图标内缓缓移动的星空 | 物品图标 |
| Eternal（永恒） | 缓慢流动的光带与闪光 | 物品图标 |
| Unstable（不稳定） | 闪烁、噼啪作响的噪点 | 物品图标 |

## 降低特效

在 `config/gtna.yaml` 的 `client` 部分：

| 选项 | 默认值 | 作用 |
|---|---|---|
| `itemHalo` | `true` | 绘制光环 |
| `itemGlowEdge` | `true` | 绘制发光边缘 |
| `itemShaderEffects` | `true` | 绘制 cosmic、eternal、unstable 着色器 |
| `itemEffectSpeed` | `100` | 动画速度百分比，0 至 400（0 为静止） |

## 整合包与资源包作者

**物品模型：**五个模型加载器 `gtna:halo`、`gtna:glow_edge`、`gtna:cosmic`、`gtna:eternal`、`gtna:unstable` 可以为任意物品模型添加特效。

**KubeJS**（`kubejs/client_scripts`，每次 F3+T 都会重新运行）：

```js
GTNAClientEvents.itemEffects(event => {
  // GTCEu 材料的所有形态
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  // 单个物品；替换其模型自带的特效
  event.item('kubejs:my_core').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('gtceu:gtna_spacetime_ingot').eternal().mask('gtna:mask/cosmic').speed(0.5)
  event.item('gtceu:gtna_chaos_matter_dust').clear()
})
```

| 方法 | 含义 |
|---|---|
| `halo(argb, 大小)` | 光环，半径以物品像素计 |
| `glowEdge(argb)`、`glowEdge(argb, 宽度)` | 发光轮廓 |
| `cosmic()`、`eternal()`、`unstable()` | 着色器特效 |
| `color(argb)`、`colors(主色, 副色)` | 着色；`0` 保留默认配色 |
| `pulse(true)` | 让光环脉动 |
| `speed(x)` | 动画速度倍率 |
| `mask(纹理)`、`texture(纹理)` | 着色器遮罩或光环纹理；默认使用物品自身轮廓 |
| `clear()` | 移除该物品的全部特效 |
