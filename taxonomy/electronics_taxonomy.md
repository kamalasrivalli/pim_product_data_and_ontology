# Electronics Product Taxonomy

## 1. Purpose

This taxonomy organises an electronics product catalogue into a hierarchical classification structure. It provides a consistent framework for categorising products in a Product Information Management (PIM) system.

## 2. Taxonomy Hierarchy

```text
Electronics
│
├── Computers
│   ├── Laptops
│   └── Desktops
│
├── Mobile Devices
│   ├── Smartphones
│   ├── Tablets
│   └── Smartwatches
│
├── Audio
│   ├── Headphones
│   ├── Earbuds
│   └── Speakers
│
├── Accessories
│   ├── Chargers
│   ├── Keyboards
│   └── Mice
│
└── Smart Home
    ├── Smart Cameras
    └── Smart Bulbs
```

## 3. Classification Principles

- Each product should be assigned to an appropriate category based on its primary product type.
- Categories should represent product types rather than product characteristics.
- Attributes such as brand, colour, connectivity and memory should be modelled separately.
- The hierarchy should remain understandable and scalable as new products are introduced.

## 4. Product Attributes

| Attribute | Example | Attribute type |
|---|---|---|
| Brand | Lenovo | Product attribute |
| RAM | 16 GB | Technical |
| Storage | 512 GB | Technical |
| Colour | Black | Physical |
| Connectivity | Wi-Fi, Bluetooth | Technical |
| Weight | 1.5 kg | Physical |

## 5. Classification Examples

| Product | Assigned category |
|---|---|
| Lenovo ThinkPad E14 | Computers > Laptops |
| Apple iPhone | Mobile Devices > Smartphones |
| Samsung Galaxy Tab | Mobile Devices > Tablets |
| Sony Wireless Headphones | Audio > Headphones |
| Logitech Mouse | Accessories > Mice |

## 6. Taxonomy and PIM Relationship

The taxonomy provides the category structure used to organise products in the PIM system.

Product attributes describe individual product characteristics, while product families define the attribute sets required for particular product types.

## 7. Future Considerations

- Category governance and naming conventions.
- Handling products that could belong to multiple categories.
- Multilingual category labels.
- Mapping external classification standards.
- Taxonomy versioning and maintenance.