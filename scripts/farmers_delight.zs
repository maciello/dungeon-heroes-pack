import crafttweaker.api.food.FoodProperties;
import crafttweaker.api.food.FoodPropertiesPossibleEffect;
import crafttweaker.api.item.IItemStack;
import crafttweaker.api.entity.effect.MobEffectInstance;
import crafttweaker.api.villagers.VillagerTrades;


//Fix Cleric Villager (Issue with revive Star)

villagerTrades.removeAllTrades(<profession:minecraft:cleric>, 1);
villagerTrades.addTrade(<profession:minecraft:cleric>, 1, 2, <item:waystones:warp_dust>, 12, 2, 0.05);
villagerTrades.addTrade(<profession:minecraft:cleric>, 1, 1, <item:minecraft:redstone> * 2, 12, 2, 0.05);
villagerTrades.addTrade(<profession:minecraft:cleric>, 1, <item:minecraft:rotten_flesh> * 32, <item:minecraft:emerald>, 16, 2, 0.05);

//Add Trades to Bartender

villagerTrades.removeAllTrades(<profession:village_taverns:bartender>, 1);

villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 2, <item:brewinandchewin:tankard> * 4, 8, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 4, <item:minecraft:cooked_beef>, 12, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 2, <item:minecraft:bread>, 12, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 1, <item:farmersdelight:cooked_mutton_chops>, 12, 3, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 1, <item:farmersdelight:cooked_bacon>, 12, 3, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 2, <item:minecraft:cooked_chicken>, 12, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 2, <item:minecraft:cooked_rabbit>, 12, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 2, <item:brewinandchewin:flaxen_cheese_wedge>, 12, 5, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 1, 8, <item:brewinandchewin:keg>, 4, 5, 0.05);

villagerTrades.addTrade(<profession:village_taverns:bartender>, 2, 10, <item:brewinandchewin:flaxen_cheese_wheel>, 6, 15, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 2, 10, <item:brewinandchewin:pizza>, 6, 15, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 2, 10, <item:brewinandchewin:quiche>, 6, 15, 0.05);

villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:brewinandchewin:beer>, 6, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:brewinandchewin:saccharine_rum>, 6, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:brewinandchewin:mead>, 6, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:brewinandchewin:pale_jane>, 6, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:farmersdelight:roast_chicken_block>, 6, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 3, 24, <item:farmersdelight:shepherds_pie_block>, 6, 30, 0.05);

villagerTrades.addTrade(<profession:village_taverns:bartender>, 4, 32, <item:brewinandchewin:heating_cask>, 4, 30, 0.05);
villagerTrades.addTrade(<profession:village_taverns:bartender>, 4, 32, <item:brewinandchewin:ice_crate>, 4, 30, 0.05);

villagerTrades.addTrade(<profession:village_taverns:bartender>, 5, 40, <item:brewinandchewin:fiery_fondue_pot>, 2, 30, 0.05);

// ━━━━━━━━━━━━━━━━━━━━ Food Changes ━━━━━━━━━━━━━━━━━━━━

// 6000 - 5 Mins
// 3600 - 3 Mins

//Tier 1 Melee
<item:farmersdelight:beef_stew>.definition.food = FoodProperties.create(10, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:strength>, 3600, 0), 1)]);
//Tier 2 Melee
<item:farmersdelight:steak_and_potatoes>.definition.food = FoodProperties.create(12, 19, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:strength>, 3600, 1), 1)]);

//Tier 1 Phyisical Crit
<item:mynethersdelight:plate_of_stuffed_hoglin_ham>.definition.food = FoodProperties.create(12, 19, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:critical_strike:chance>, 3600, 0), 1)]);

//Tier 1 Ranged
<item:farmersdelight:roast_chicken>.definition.food = FoodProperties.create(12, 19, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:ranged_weapon:haste>, 3600, 0), 1)]);
//Tier 2 Ranged
<item:farmersdelight:shepherds_pie>.definition.food = FoodProperties.create(14, 22, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:ranged_weapon:damage>, 3600, 1), 1)]);

//Tier 1 Fire Magic
<item:mynethersdelight:spicy_hoglin_stew>.definition.food = FoodProperties.create(12, 19, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 2400, 0), 1),
//  FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 1200, 1), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:fire>, 3600, 0), 1)]);
<item:brewinandchewin:fiery_fondue>.definition.food = FoodProperties.create(14, 22, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 8400, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:fire>, 3600, 0), 1)]);
//Tier 2 Fire Magic
<item:mynethersdelight:spicy_curry>.definition.food = FoodProperties.create(14, 22, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
//  FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 6000, 1), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:fire>, 3600, 1), 1)]);

//Tier 1 Arcane Magic
<item:mynethersdelight:plate_of_ghasta_with_cream>.definition.food = FoodProperties.create(8, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 1200, 0), 1),
//  FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 1200, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:arcane>, 3600, 0), 1)]);
//Tier 2 Arcane Magic
<item:mynethersdelight:blue_tenderloin_steak>.definition.food = FoodProperties.create(9, 15, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:nausea>, 300, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 1200, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:arcane>, 6000, 1), 1)]);

//Tier 1 Ice Magic
<item:farmersdelight:fish_stew>.definition.food = FoodProperties.create(10, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:frost>, 3600, 0), 1)]);
//Tier 2 Ice Magic
<item:farmersdelight:squid_ink_pasta>.definition.food = FoodProperties.create(14, 22, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:frost>, 3600, 1), 1)]);

//Tier 1 Healing Magic
<item:farmersdelight:fruit_salad>.definition.food = FoodProperties.create(6, 7, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:regeneration>, 100, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:healing>, 3600, 0), 1)]);
<item:farmersdelight:mixed_salad>.definition.food = FoodProperties.create(6, 7, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:regeneration>, 100, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:healing>, 3600, 0), 1)]);
//Tier 2 Healing Magic
<item:farmersdelight:grilled_salmon>.definition.food = FoodProperties.create(14, 22, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:healing>, 3600, 1), 1)]);

//Tier 1 Generic Magic
<item:farmersdelight:mushroom_rice>.definition.food = FoodProperties.create(10, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:critical_chance>, 3600, 0), 1)]);
<item:farmersdelight:pumpkin_soup>.definition.food = FoodProperties.create(10, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:haste>, 3600, 0), 1)]);
//Tier 2 Generic Magic
<item:farmersdelight:honey_glazed_ham>.definition.food = FoodProperties.create(14, 11, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:haste>, 3600, 1), 1)]);
<item:mynethersdelight:fried_hoglin_chop>.definition.food = FoodProperties.create(12, 11, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 2400, 0), 1),
//  FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 1200, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:critical_chance>, 3600, 1), 1)]);



// Brewin and Chewin

<item:brewinandchewin:red_rum>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 2400, 2), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:fire>, 1200, 1), 1)]);

<item:brewinandchewin:pale_jane>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 2400, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:healing>, 1200, 1), 1)]);

<item:brewinandchewin:glittering_grenadine>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 2400, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:glowing>, 600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:night_vision>, 600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:arcane>, 1200, 1), 1)]);

<item:brewinandchewin:salty_folly>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 3600, 1), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:water_breathing>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:frost>, 1200, 1), 1)]);

<item:brewinandchewin:vodka>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:critical_damage>, 1200, 1), 1)]);

<item:brewinandchewin:steel_toe_stout>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 2400, 2), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:resistance>, 1200, 0), 1)]);

<item:brewinandchewin:beer>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 2400, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:strength>, 1200, 0), 1)]);

<item:brewinandchewin:withering_dross>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 3600, 2), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:blindness>, 200, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:weakness>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:slowness>, 3000, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:wither>, 1200, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:spell_power:critical_chance>, 1200, 4), 1)]);

<item:brewinandchewin:saccharine_rum>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 3600, 1), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 2400, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:sweet_heart>, 3600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:ranged_weapon:damage>, 1200, 1), 1)]);



// Temporary Comfort -> Nourishment changes

<item:brewinandchewin:rice_wine>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:tipsy>, 2400, 2), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:brewinandchewin:intoxication>, 1800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 1200, 0), 1)]);
    
<item:brewinandchewin:creamy_onion_soup>.definition.food = FoodProperties.create(0, 0, false, 1, <item:brewinandchewin:tankard>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1)]);

<item:mynethersdelight:strider_stew>.definition.food = FoodProperties.create(8, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:fire_resistance>, 800, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 1200, 0), 1)]);
    
<item:mynethersdelight:crimson_stroganoff>.definition.food = FoodProperties.create(8, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:minecraft:fire_resistance>, 600, 0), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 2400, 0), 1)]);
    
<item:mynethersdelight:spicy_noodle_soup>.definition.food = FoodProperties.create(8, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 1200, 1), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 6000, 0), 1)]);
    
<item:mynethersdelight:rock_soup>.definition.food = FoodProperties.create(8, 17, false, 1, <item:minecraft:air>, [
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:mynethersdelight:b_pungent>, 1200, 2), 1),
    FoodPropertiesPossibleEffect.of(MobEffectInstance.of(<mobeffect:farmersdelight:nourishment>, 3600, 0), 1)]);


<tag:item:c:foods/milk>.add(<tag:item:c:drinks/milk>);