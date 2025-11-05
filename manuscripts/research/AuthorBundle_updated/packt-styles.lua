--[[
PacktPub Style Mapping Filter
Maps standard Pandoc elements to PacktPub [PACKT] styles
]]--

function Header(el)
  -- Map headers to PacktPub heading styles
  local style_name = ''
  if el.level == 1 then
    style_name = 'Heading 1 [PACKT]'
  elseif el.level == 2 then
    style_name = 'Heading 2 [PACKT]'
  elseif el.level == 3 then
    style_name = 'Heading 3 [PACKT]'
  elseif el.level == 4 then
    style_name = 'Heading 4 [PACKT]'
  end
  el.attr.attributes['custom-style'] = style_name
  return el
end

function Para(el)
  -- Map paragraphs to Normal [PACKT] style
  el.attr = el.attr or pandoc.Attr()
  el.attr.attributes['custom-style'] = 'Normal [PACKT]'
  return el
end

function CodeBlock(el)
  -- Map code blocks to Code [PACKT] style
  el.attr.attributes['custom-style'] = 'Code [PACKT]'
  return el
end

function Code(el)
  -- Inline code uses Code In Text [PACKT] character style
  -- Note: This requires wrapping in a span with custom-style
  return pandoc.Span(el, {['custom-style'] = 'Code In Text [PACKT]'})
end

function BulletList(items)
  -- Map bullet list items to Bullet [PACKT]
  local new_items = {}
  for i, item in ipairs(items) do
    local new_blocks = {}
    for j, block in ipairs(item) do
      if block.t == 'Plain' or block.t == 'Para' then
        block.attr = block.attr or pandoc.Attr()
        block.attr.attributes['custom-style'] = 'Bullet [PACKT]'
      end
      table.insert(new_blocks, block)
    end
    table.insert(new_items, new_blocks)
  end
  return pandoc.BulletList(new_items)
end

function OrderedList(items)
  -- Map numbered lists to Numbered Bullet [PACKT]
  local new_items = {}
  for i, item in ipairs(items) do
    local new_blocks = {}
    for j, block in ipairs(item) do
      if block.t == 'Plain' or block.t == 'Para' then
        block.attr = block.attr or pandoc.Attr()
        block.attr.attributes['custom-style'] = 'Numbered Bullet [PACKT]'
      end
      table.insert(new_blocks, block)
    end
    table.insert(new_items, new_blocks)
  end
  return pandoc.OrderedList(new_items)
end

function BlockQuote(el)
  -- Map block quotes to Quote [PACKT]
  for i, block in ipairs(el.content) do
    if block.t == 'Para' then
      block.attr = block.attr or pandoc.Attr()
      block.attr.attributes['custom-style'] = 'Quote [PACKT]'
    end
  end
  return el
end

function Strong(el)
  -- Map strong/bold to Key Word [PACKT] character style
  return pandoc.Span(el.content, {['custom-style'] = 'Key Word [PACKT]'})
end

function Emph(el)
  -- Map emphasis/italic to Italics [PACKT] character style
  return pandoc.Span(el.content, {['custom-style'] = 'Italics [PACKT]'})
end

function Link(el)
  -- Map links to URL [PACKT] character style
  return pandoc.Span(el.content, {['custom-style'] = 'URL [PACKT]'})
end

-- Return all filters
return {
  {Header = Header},
  {Para = Para},
  {CodeBlock = CodeBlock},
  {Code = Code},
  {BulletList = BulletList},
  {OrderedList = OrderedList},
  {BlockQuote = BlockQuote},
  {Strong = Strong},
  {Emph = Emph},
  {Link = Link}
}
